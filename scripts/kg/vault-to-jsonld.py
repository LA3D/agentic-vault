#!/usr/bin/env python3
"""vault-to-jsonld.py — Batch convert vault frontmatter to JSON-LD @graph.

Usage:
    python3 vault-to-jsonld.py [--vault PATH] [--output PATH] [--stats]

Walks the vault, extracts YAML frontmatter from .md files, strips wikilinks,
mints URIs, applies @context, and outputs a single JSON-LD document with an
@graph array. Pipe to `riot` for Turtle conversion:

    python3 vault-to-jsonld.py | riot --syntax=jsonld --output=turtle > vault-graph.ttl
"""

import json
import os
import re
import sys
import urllib.parse
import yaml
from pathlib import Path

# --- Configuration ---

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent  # scripts/kg/ -> vault root
CONTEXT_FILE = SCRIPT_DIR / "vault-context.jsonld"
ONTOLOGY_FILE = SCRIPT_DIR / "vault-ontology.ttl"
OUTPUT_FILE = None  # stdout by default

# Directories to skip entirely
SKIP_DIRS = {
    '.obsidian', '.git', '.trash', '.claude',
    'node_modules', 'scripts', 'Templates',
    '04 - Archive',
}

# Edge fields whose string values become URI references
EDGE_FIELDS = {
    'up', 'area', 'concept', 'source', 'extends',
    'supports', 'criticizes', 'implementation', 'related',
    'author', 'affiliation', 'collaborator',
}

# Vault ontology namespace
VAULT_NS = "https://example.com/vault/ontology#"


def load_type_map(ontology_path):
    """Derive TYPE_MAP from vault-ontology.ttl skos:notation values.

    Parses the ontology to find classes with skos:notation and builds
    a mapping from notation string to compact IRI (vault:ClassName).
    The ontology is the source of truth for this mapping.
    """
    type_map = {}
    if not ontology_path.exists():
        print(f"Warning: ontology not found at {ontology_path}, using empty type map",
              file=sys.stderr)
        return type_map

    # Simple regex-based extraction — avoids rdflib dependency.
    # Looks for patterns like:
    #   vault:Project a rdfs:Class, skos:Concept ;
    #       ...
    #       skos:notation "project" ;
    content = ontology_path.read_text(encoding='utf-8')

    # Find all (vault:ClassName ... skos:notation "value") pairs
    # Split on blank lines to get per-resource blocks
    current_class = None
    for line in content.split('\n'):
        line = line.strip()
        # Match "vault:ClassName a rdfs:Class"
        m = re.match(r'^(vault:\w+)\s+a\s+rdfs:Class', line)
        if m:
            current_class = m.group(1)
        # Match 'skos:notation "value"'
        m = re.match(r'skos:notation\s+"([^"]+)"', line)
        if m and current_class:
            type_map[m.group(1)] = current_class
        # Reset on blank line or new resource
        if line == '' or (line and not line.startswith(('skos:', 'rdfs:', 'owl:'))
                                                       and 'a rdfs:Class' not in line
                          and not line.endswith(('.',  ';'))):
            if line == '':
                current_class = None

    return type_map


# Build TYPE_MAP from ontology at import time
TYPE_MAP = load_type_map(ONTOLOGY_FILE)

# Subfolder prefixes for URI disambiguation
DISAMBIGUATE_PARENTS = {
    'Literature', 'Theory', 'Implementation', 'External Resources',
    'Methods', 'Memory Architecture', 'Findings',
}

# --- Helpers ---

WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')


def title_to_slug(title):
    """Convert a note title to a URI-safe slug.
    Spaces -> hyphens, percent-encode the rest. Preserves / for path segments."""
    parts = title.strip().split('/')
    slugged = []
    for p in parts:
        p = p.replace(' ', '-')
        p = urllib.parse.quote(p, safe='-._~')
        slugged.append(p)
    return '/'.join(slugged)


def strip_wikilink(s):
    """Strip [[ ]] from a string, handle [[Note|display]] -> Note.
    Also strips #fragment (heading references) and .md extension."""
    s = s.strip()
    m = WIKILINK_RE.search(s)
    if m:
        inner = m.group(1)
        # [[Note|display text]] -> Note
        if '|' in inner:
            inner = inner.split('|')[0]
        # [[Note#heading]] -> Note (heading refs aren't separate nodes)
        if '#' in inner:
            inner = inner.split('#')[0]
        # [[Note.md]] -> Note (strip file extension)
        if inner.endswith('.md'):
            inner = inner[:-3]
        return inner.strip()
    # Not a wikilink — return as-is
    return s


def value_to_ref(v, title_uri_map=None):
    """Convert a wikilink string to a JSON-LD @id reference.

    If title_uri_map is provided, resolve bare titles to their canonical
    URI (with parent-directory prefix). This fixes the identity split where
    [[Note Title]] and the note's own @id (e.g., Theory/Note-Title) differ.
    """
    title = strip_wikilink(v)

    if title_uri_map:
        # Strip any path prefix from the wikilink for lookup
        # [[Theory/Agent Action Paradigms...]] → "Agent Action Paradigms..."
        bare_title = title.split('/')[-1] if '/' in title else title
        if bare_title in title_uri_map:
            return {'@id': title_uri_map[bare_title]}
        # Also try the full path-prefixed form
        if title in title_uri_map:
            return {'@id': title_uri_map[title]}

    # Fallback: just slugify (used during first pass or for unknown titles)
    return {'@id': title_to_slug(title)}


def process_edge_value(v, title_uri_map=None):
    """Process an edge field value: string or list of strings -> @id refs.

    Only wikilink-wrapped values ([[...]]) become URI references.
    Plain strings (e.g., Readwise source: "twitter") are dropped from
    edge fields — they're metadata, not graph relationships.
    Empty/null values are also dropped.
    """
    if v is None or v == '':
        return None
    if isinstance(v, str):
        if '[[' in v:
            return value_to_ref(v, title_uri_map)
        # Plain string in edge field — not a vault relationship, skip
        return None
    if isinstance(v, list):
        result = []
        for item in v:
            if isinstance(item, str) and '[[' in item:
                result.append(value_to_ref(item, title_uri_map))
            # Plain strings and non-string items in edge lists are skipped
        return result if result else None
    return v


def extract_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file. Returns dict or None."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().rstrip('\n')
            if first_line != '---':
                return None
            lines = []
            for line in f:
                if line.rstrip('\n') == '---':
                    break
                lines.append(line)
            else:
                # Hit EOF without closing ---
                return None
        if not lines:
            return None
        return yaml.safe_load(''.join(lines))
    except (yaml.YAMLError, UnicodeDecodeError, OSError):
        return None


def note_to_jsonld(filepath, vault_root, title_uri_map=None):
    """Convert a single note's frontmatter to a JSON-LD node dict."""
    fm = extract_frontmatter(filepath)
    if not fm or not isinstance(fm, dict):
        return None

    # Skip notes without type — they have no semantic role in the graph
    if 'type' not in fm and 'noteType' not in fm:
        return None

    doc = dict(fm)

    # Normalize noteType -> type (legacy fix)
    if 'noteType' in doc and 'type' not in doc:
        doc['type'] = doc.pop('noteType')
    elif 'noteType' in doc:
        del doc['noteType']

    # Remove legacy Dataview fields
    for legacy in ('relatedConcepts', 'relatedLiterature', 'implementations'):
        doc.pop(legacy, None)

    # Generate @id from filename with optional parent disambiguation
    basename = filepath.stem
    slug = title_to_slug(basename)

    parent = filepath.parent.name
    if parent in DISAMBIGUATE_PARENTS:
        slug = f'{title_to_slug(parent)}/{slug}'

    doc['@id'] = slug

    # Map type to ontology IRI
    if 'type' in doc:
        t = doc['type']
        doc['type'] = TYPE_MAP.get(t, f'vault:{t}')

    # Transform edge fields to @id references (with URI resolution)
    # Drop fields that resolve to None (plain strings, empty values)
    for field in EDGE_FIELDS:
        if field in doc:
            resolved = process_edge_value(doc[field], title_uri_map)
            if resolved is None:
                del doc[field]
            else:
                doc[field] = resolved

    # Add title from filename
    doc['title'] = basename

    # Convert date objects to strings (PyYAML parses dates automatically)
    for k, v in doc.items():
        if hasattr(v, 'isoformat'):
            doc[k] = v.isoformat()

    # Remove fields that don't belong in the graph
    doc.pop('cssclasses', None)
    doc.pop('aliases', None)
    doc.pop('publish', None)

    return doc


def should_skip(dirpath, vault_root):
    """Check if a directory should be skipped."""
    rel = os.path.relpath(dirpath, vault_root)
    parts = Path(rel).parts
    return any(p in SKIP_DIRS for p in parts)


def build_title_uri_map(vault_root):
    """First pass: build a mapping from note title (basename) to canonical URI slug.

    This resolves the identity split where a note's own @id includes a parent
    directory prefix (e.g., Theory/Note-Title) but wikilinks referencing it
    use bare titles (e.g., [[Note Title]] → Note-Title without Theory/).
    """
    title_map = {}
    for dirpath, dirnames, filenames in os.walk(vault_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if should_skip(dirpath, vault_root):
            continue
        for fname in sorted(filenames):
            if not fname.endswith('.md'):
                continue
            fpath = Path(dirpath) / fname
            basename = fpath.stem
            slug = title_to_slug(basename)
            parent = fpath.parent.name
            if parent in DISAMBIGUATE_PARENTS:
                slug = f'{title_to_slug(parent)}/{slug}'
            # Map bare title → canonical slug (with parent prefix if applicable)
            title_map[basename] = slug
    return title_map


def build_graph(vault_root, stats):
    """Walk the vault and build the @graph array.

    Two-pass process:
    1. Build title→URI mapping (so wikilink references resolve to canonical URIs)
    2. Process notes with edge resolution against the mapping
    """
    # Pass 1: collect all note URIs
    title_uri_map = build_title_uri_map(vault_root)

    # Pass 2: process notes with URI-aware edge resolution
    graph = []
    for dirpath, dirnames, filenames in os.walk(vault_root):
        # Prune skipped directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        if should_skip(dirpath, vault_root):
            continue

        for fname in sorted(filenames):
            if not fname.endswith('.md'):
                continue

            fpath = Path(dirpath) / fname
            stats['total'] += 1

            node = note_to_jsonld(fpath, vault_root, title_uri_map)
            if node is None:
                stats['skipped'] += 1
                continue

            graph.append(node)
            stats['processed'] += 1

            # Track types
            t = node.get('type', 'unknown')
            stats['types'][t] = stats['types'].get(t, 0) + 1

    return graph


# --- Main ---

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Convert vault frontmatter to JSON-LD')
    parser.add_argument('--vault', type=Path, default=VAULT_ROOT, help='Vault root directory')
    parser.add_argument('--output', type=Path, default=None, help='Output file (default: stdout)')
    parser.add_argument('--stats', action='store_true', help='Print stats to stderr')
    parser.add_argument('--skip-riot', action='store_true', help='Output JSON-LD only, skip riot')
    args = parser.parse_args()

    vault_root = args.vault.resolve()
    if not (vault_root / 'VAULT-INDEX.md').exists():
        print(f"Error: {vault_root} doesn't look like the vault (no VAULT-INDEX.md)", file=sys.stderr)
        sys.exit(1)

    # Load @context
    with open(CONTEXT_FILE) as f:
        ctx = json.load(f)['@context']

    stats = {'total': 0, 'processed': 0, 'skipped': 0, 'types': {}}
    graph = build_graph(vault_root, stats)

    # Build the JSON-LD document
    doc = {
        '@context': ctx,
        '@graph': graph,
    }

    output_json = json.dumps(doc, indent=2, ensure_ascii=False)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w') as f:
            f.write(output_json)
            f.write('\n')
        if args.stats:
            print(f"JSON-LD written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    if args.stats:
        print(f"\n--- Stats ---", file=sys.stderr)
        print(f"Total .md files: {stats['total']}", file=sys.stderr)
        print(f"Processed (have type): {stats['processed']}", file=sys.stderr)
        print(f"Skipped (no type/frontmatter): {stats['skipped']}", file=sys.stderr)
        print(f"\nTypes:", file=sys.stderr)
        for t, count in sorted(stats['types'].items(), key=lambda x: -x[1]):
            print(f"  {t}: {count}", file=sys.stderr)


if __name__ == '__main__':
    main()
