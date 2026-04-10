---
name: vault-kg
description: "Query the vault's knowledge graph via raw SPARQL — multi-hop relationships, concept chains, area rollups, and custom graph queries. Use this skill for direct SPARQL queries, rebuilding the graph, or answering structural questions that require graph traversal across dozens of files. Also use when the user says 'rebuild the graph', 'run SPARQL', 'query the knowledge graph', or 'graph query'. For vault health checks (orphans, dangling refs, type validity), use /audit instead. For structured note retrieval (what do we know about X, find related notes), use /retrieve instead. Trigger proactively when navigating the vault and a raw graph query would be faster than sequential file reads."
---

# Vault Knowledge Graph — Semantic Navigation Skill

Query the vault's typed relationships as a SPARQL knowledge graph. The graph is built from YAML frontmatter via a JSON-LD pipeline, producing ~9000 base triples + ~500 materialized triples from 670+ notes.

## When to use this vs other tools

| Question type | Tool | Example |
|---|---|---|
| **Content**: "what's in a file?" | Obsidian CLI, grep, Glob, Read | "Find the note about context graphs" |
| **Structure**: "how do things connect?" | This skill (SPARQL) | "What literature supports context graphs?" |
| **Topology → Content** | KG → Read | "Find all projects serving Research & Scholarship, then read their status" |

## Infrastructure

```
scripts/kg/
├── build-graph.sh            # Full pipeline: extract → convert → materialize → validate
├── vault-to-jsonld.py        # Batch processor (Python)
├── vault-context.jsonld      # @context mapping frontmatter → RDF
├── vault-ontology.ttl        # SKOS + RDFS vocabulary (source of truth for types/edges)
├── vault-shapes.ttl          # SHACL validation + materialization rules
├── vault-queries.ttl         # Self-describing query catalog (SIB/UniProt pattern)
├── sparql/                   # Standalone .rq files (extracted from catalog)
├── vault-graph.ttl           # Base graph (gitignored, generated)
├── vault-graph-full.ttl      # Base + materialized triples (gitignored, generated)
└── validation-report.ttl     # SHACL validation report (gitignored, generated)
```

Tools: `arq`, `riot`, `shacl` (Apache Jena 6.0.0, all at `/opt/homebrew/bin/`)

## Step 1: Ensure the graph is fresh

```bash
if [[ ! -f scripts/kg/vault-graph-full.ttl ]]; then
    bash scripts/kg/build-graph.sh --stats
fi
```

Rebuild when notes have been added/modified this session:
```bash
bash scripts/kg/build-graph.sh --stats              # full (with validation)
bash scripts/kg/build-graph.sh --stats --skip-validate  # faster (skip SHACL)
```

Pipeline takes ~8-9 seconds. Always query `vault-graph-full.ttl` (includes materialized inverse edges, area inheritance, hub detection).

## Step 2: Run queries

### Pre-built queries (preferred)

Standalone `.rq` files in `scripts/kg/sparql/` — run directly:

```bash
cd scripts/kg
arq --data=vault-graph-full.ttl --query=sparql/hub-notes.rq
arq --data=vault-graph-full.ttl --query=sparql/orphan-notes.rq
arq --data=vault-graph-full.ttl --query=sparql/concept-chain.rq
```

**Parameterized queries** have placeholders — use `sed` to fill them:

```bash
# Replace AREA_SUBSTRING
sed 's/AREA_SUBSTRING/Research/' sparql/notes-by-area.rq | arq --data=vault-graph-full.ttl --query=-

# Replace SEARCH_TERM
sed 's/SEARCH_TERM/some topic/' sparql/search-by-title.rq | arq --data=vault-graph-full.ttl --query=-

# Replace CONCEPT_SUBSTRING
sed 's/CONCEPT_SUBSTRING/progressive disclosure/' sparql/literature-for-concept.rq | arq --data=vault-graph-full.ttl --query=-

# Replace NOTE_URI (full URI required)
sed 's|NOTE_URI|https://example.com/vault/notes/Theory/My-Concept|' sparql/note-neighborhood.rq | arq --data=vault-graph-full.ttl --query=-
```

### Available queries by category

| Category | File | Placeholders | What it finds |
|---|---|---|---|
| **Navigation** | `notes-by-type.rq` | none | Type distribution overview |
| | `notes-by-area.rq` | `AREA_SUBSTRING` | Notes serving an area of focus |
| | `children-of.rq` | `PARENT_SLUG` | Notes under a MOC/parent |
| | `ancestors-of.rq` | `NOTE_SLUG` | Walk up hierarchy to root |
| **Discovery** | `search-by-title.rq` | `SEARCH_TERM` | Title substring search with edges |
| | `notes-by-tag.rq` | `TAG_VALUE` | Notes with a specific tag |
| **Research** | `concept-chain.rq` | none | Literature → concept → implementation chains |
| | `supports-criticizes.rq` | none | Full argument map |
| | `extension-chains.rq` | none | Theory lineage (extends edges) |
| | `literature-for-concept.rq` | `CONCEPT_SUBSTRING` | Papers referencing a concept |
| **Quality** | `orphan-notes.rq` | none | Notes with no incoming edges |
| | `hub-notes.rq` | none | Most-connected notes |
| | `projects-missing-area.rq` | none | Pullein compliance check |
| | `graph-stats.rq` | none | Total triples and typed notes |
| **Retrieve** | `concept-neighborhood.rq` | `CONCEPT_SUBSTRING` | All notes connected to a concept |
| | `note-neighborhood.rq` | `NOTE_URI` | 2-hop neighborhood of a note |
| | `cold-neighbors.rq` | `NOTE_URI` | Underexplored nearby notes |
| | `cross-moc-bridges.rq` | `NOTE_URI` | Notes bridging different MOCs |

### Custom inline queries

For ad-hoc questions not covered by the catalog, write inline SPARQL:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=- <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?title ?type WHERE {
    ?note dcterms:title ?title .
    ?note a ?type .
} LIMIT 10
SPARQL
```

### Vault ontology predicates

| Predicate | Meaning | Materialized inverse |
|---|---|---|
| `vault:up` | Parent in hierarchy | (transitive closure materialized) |
| `vault:area` | Area of focus served | (inherited down hierarchy) |
| `vault:concept` | Related concept | `vault:conceptOf` |
| `vault:source` | Literature source | — |
| `vault:extends` | Builds upon | — |
| `vault:supports` | Validates/agrees | `vault:supportedBy` |
| `vault:criticizes` | Challenges/opposes | `vault:criticizedBy` |
| `vault:implementation` | Code implementing this | — |
| `vault:related` | General connection | — |
| `vault:author` | Author of work | `vault:authorOf` |
| `vault:affiliation` | Organization | — |
| `vault:collaborator` | Project collaborator | — |
| `vault:isHub` | ≥10 inbound edges | (materialized, boolean) |

Read `scripts/kg/vault-ontology.ttl` for full definitions, domain/range constraints, and scope notes.

## Step 3: From results to vault files

SPARQL returns `dcterms:title` values matching note filenames (minus `.md`). To find the actual file:

1. Use Glob: `**/<title>.md`
2. URI slugs encode paths: `Theory/My-Concept` → file is in a `Theory/` subfolder as `My Concept.md`
3. Then use Read to access content

## Step 4: Validation

Run SHACL validation to find structural issues:

```bash
cd scripts/kg && shacl validate --shapes=vault-shapes.ttl --data=vault-graph-full.ttl
```

Finds: missing `area:` on projects, missing `up:` on MOCs/literature, dangling references. Summarize violations:

```bash
shacl validate --shapes=vault-shapes.ttl --data=vault-graph-full.ttl 2>&1 \
  | grep "sh:resultMessage" | sed 's/.*sh:resultMessage *"//' | sed 's/".*//' \
  | sort | uniq -c | sort -rn | head -20
```

## Query catalog as source of truth

The standalone `.rq` files are extracted from `vault-queries.ttl` (the self-describing catalog in SIB/UniProt pattern). If you need a query not in `sparql/`, check the catalog first:

```bash
# Browse available queries and their descriptions
grep -A1 'rdfs:comment' scripts/kg/vault-queries.ttl
```

For truly novel queries, write inline SPARQL using the predicates table above. If a new query proves reusable, it should be added to both the catalog and `sparql/`.

## URI conventions

- Base: `https://example.com/vault/notes/`
- Ontology: `https://example.com/vault/ontology#`
- Slugs: spaces → hyphens, special chars percent-encoded
- Examples: `Research-&-Scholarship`, `Theory/My-Concept`, `Literature/@smith-2025-example`
