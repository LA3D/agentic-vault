# Typed Relationships and Note Typing

Type taxonomy and typed relationship vocabulary for this vault. Edge fields in YAML frontmatter define the vault's knowledge graph — consumed by the KG pipeline (`scripts/kg/`) for SPARQL queries and by Claude Code for navigation. The Breadcrumbs Obsidian plugin can optionally render these as visual hierarchy, but the vocabulary is the vault's own, defined in `scripts/kg/vault-ontology.ttl` and mapped to RDF via `scripts/kg/vault-context.jsonld`.

---

## Property Standardization

Use `type:` in frontmatter (not `noteType:`). Canonical values:

| Category | Values | Used in |
|----------|--------|---------|
| Knowledge notes | `theory-note`, `concept-note`, `method-note`, `finding`, `implementation-note` | 03 - Resources/[topic]/ |
| Literature | `literature-note`, `book-note`, `author-note` | 03 - Resources/Literature/ |
| Entity | `person`, `organization` | 03 - Resources/People/, 03 - Resources/People/Organizations/ |
| External | `external-resource`, `tool` | External Resources/ |
| Navigation | `moc`, `index` | MOCs, sub-indexes |
| Area | `area` | 02 - Areas of Focus/ |
| Project | `project`, `plan`, `decision` | 01 - Projects/ |
| Reference | `reference`, `workflow`, `course-notes` | 03 - Resources/Obsidian Reference/, Courses/ |
| Other | `recipe-collection`, `fleeting-note` | Cooking & Recipes/, 05 - Watching/ |

### Two-Tier Literature System

Literature notes use `type: literature-note` with an optional `literatureType:` field for granularity:

| `literatureType:` value | When to use |
|-------------------------|-------------|
| `research-paper` | Standard academic research paper |
| `empirical-study` | Data-driven empirical research |
| `position-paper` | Advocacy/opinion paper |
| `benchmark-paper` | Evaluation/benchmark study |
| `working-paper` | Preprint or draft paper |
| `perspective` | Perspective or viewpoint article |
| `modeling-study` | Computational or mathematical modeling |
| `randomized-controlled-trial` | RCT or clinical trial |
| `industry-report` | Industry/technical report |
| `dissertation` | Thesis or dissertation |
| `comment` | Commentary or response |
| `blog-research` | Research-focused blog post |

**Note**: `book-note` and `author-note` remain separate `type:` values (not literatureType).

---

## Edge Fields

Populate these in YAML frontmatter to create typed relationships. Each field maps to an RDF property via `scripts/kg/vault-context.jsonld` and becomes queryable in the vault's knowledge graph:

| Field | Meaning | Use when... | Example |
|-------|---------|-------------|---------|
| `up:` | Parent in hierarchy | Note belongs to a MOC or topic group | `up: "[[Your Topic MOC]]"` |
| `area:` | Area of focus served | Project or MOC serves an area of focus | `area: "[[Research & Scholarship]]"` |
| `concept:` | Concept this relates to | Literature discusses a concept; implementation realizes a concept | `concept: "[[Example Concept]]"` |
| `implementation:` | Code/system implementing this | Concept note has a corresponding repo/experiment | `implementation: "[[Example Framework]]"` |
| `source:` | Literature source | Any note citing a paper | `source: "[[Literature/@smith-2025-example]]"` |
| `extends:` | Builds upon | Theory note extends another theory | `extends: "[[Parent Theory]]"` |
| `criticizes:` | Challenges/opposes | Paper or note argues against a claim | `criticizes: "[[Contested Claim]]"` |
| `supports:` | Validates/agrees | Paper provides evidence for a claim | `supports: "[[Validated Hypothesis]]"` |
| `related:` | Lateral connection | General connection that doesn't fit above categories | Keep as catch-all but prefer specific relations |
| `author:` | Person who authored this work | Literature note, book note, or external resource has a known author with a vault note | `author: "[[smith-jane]]"` |
| `affiliation:` | Organization a person belongs to | Person or author note has a known institutional affiliation | `affiliation: "[[Example University]]"` |
| `collaborator:` | Person collaborating on a project | Project has known collaborators with vault notes | `collaborator: "[[doe-john]]"` |

See `[[Vault Vocabulary]]` for domain/range constraints on each edge field (which note types can use which fields, and what types they should point to).

---

## Rules for Claude

### When creating ANY new note
- Always include `type:` in frontmatter with a value from the taxonomy above

### When creating projects or MOCs
- Populate `area:` to link to the area of focus they serve (e.g., `area: "[[Research & Scholarship]]"`)
- Every project should connect to at least one area — if it doesn't, question why it exists

### When creating literature notes
- Populate `concept:`, `source:`, `supports:`/`criticizes:` where applicable
- Use `up:` to link to the relevant MOC
- Add `author:` edge (wikilink to author note) if the author has a vault note. The existing `authors:` string field stays for display; `author:` is the graph edge.

### When creating author notes (`type: author-note`)
- Use for researchers, writers, and thought leaders known primarily through their work
- Location: `03 - Resources/People/lastname-firstname.md`
- Must have: `up:` (typically `[[LITERATURE-INDEX]]`), `aliases:` (all name variants — citekey patterns, social handles, display name variations)
- Should have: `affiliation:` (if institutional affiliation is known), `area:` (if relevant to a specific area of focus)
- `aliases:` is critical — it's the glue that connects literature note citekeys and body text mentions to the same node

### When creating person notes (`type: person`)
- Use for collaborators, contacts, and people known through work rather than authorship
- Location: `03 - Resources/People/lastname-firstname.md`
- Should have: `affiliation:`, `up:` (to relevant MOC or VAULT-INDEX)
- A person can also be an author — if they start publishing work you track, consider upgrading to `type: author-note`

### When creating organization notes (`type: organization`)
- Use for institutions, labs, companies that recur across multiple notes or projects
- Location: `03 - Resources/People/Organizations/org-name.md`
- Only create when the organization is referenced by 3+ notes — don't create one-off org notes
- Should have: `up:` (to `[[PEOPLE-INDEX]]` or relevant MOC)

### When creating theory/concept notes
- Populate `up:`, `extends:`, `source:` where applicable
- Add `implementation:` if code exists for this concept

### When creating implementation notes
- Populate `concept:`, `source:` where applicable

### When editing existing notes
- Opportunistically add missing `type:` and edge field properties
- Replace `noteType:` with `type:` if encountered
- Remove legacy Dataview fields (`relatedConcepts`, `relatedLiterature`, `implementations`) when found
- Don't mass-retrofit — fix notes as you touch them

### General
- Prefer specific relations (`extends:`, `supports:`, `criticizes:`) over generic `related:`
- Wikilinks in prose body are still valuable for narrative connections — frontmatter edge fields don't replace them
- Use tag-style types only in tags array (e.g., `#status/draft`), not for note typing

---

## Curator Observation Fields

Optional frontmatter fields populated by note-creation skills when ontology fit is uncertain. The `/curator` skill harvests these for review.

| Field | Values | Purpose |
|-------|--------|---------|
| `curator_status:` | `pending`, `reviewed`, `accepted`, `declined` | Processing state |
| `curator_suggested_type:` | Any canonical type value | Suggests a better type for the note |
| `curator_suggested_up:` | Wikilink to MOC/index | Suggests a better parent |
| `curator_observations:` | List of strings | Free-text reasoning behind suggestions |

### When to populate curator fields

- **Uncertain type fit**: The note straddles two types (e.g., both method and theory)
- **Missing edge type**: A key relationship doesn't map to any existing edge field
- **Domain clustering**: This is the 3rd+ note in an area that lacks a MOC
- **Scope drift**: A note's content has outgrown its type (e.g., a concept-note that's really a theory-note)
- **New vocabulary needed**: The note introduces terminology that could become a new type or literatureType

### Rules

- Fields are OPTIONAL — only populate when something noteworthy is observed
- `curator_suggested_type` must be from the canonical type taxonomy (or flag as "proposed: [new-type]")
- `curator_suggested_up` must be a wikilink to an existing or proposed MOC/index
- Notes with `curator_status: pending` are harvestable by `/curator review`
- See `[[Vault Vocabulary]]` for the full controlled vocabulary

---

## Deprecation Notes

| Old | New | Status |
|-----|-----|--------|
| `noteType:` | `type:` | Fix on contact |
| `relatedConcepts:` | `concept:` (edge field) | Remove on contact |
| `relatedLiterature:` | `source:` (edge field) | Remove on contact |
| `implementations:` | `implementation:` (edge field) | Remove on contact |
| `#type/concept` tag | `type: concept-note` frontmatter | Tag is supplementary only |

---

## Templates

Templates exist at:
- `Templates/Concept Note.md` — concept and theory notes
- `Templates/Literature Note.md` — papers and literature
- `Templates/Implementation Note.md` — code and experiments

Follow their frontmatter edge field patterns, using `type:` (not `noteType:`).

---

## Vault Reference

For a browsable in-vault reference, see: `[[Vault Vocabulary]]` in `03 - Resources/Obsidian Reference/`

---

**Related**:
- [vault-navigation.md](vault-navigation.md) — Navigation patterns
- [linking-guide.md](linking-guide.md) — Wikilink conventions and linking patterns
