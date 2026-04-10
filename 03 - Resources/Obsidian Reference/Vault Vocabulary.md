---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - ontology
  - types
---

# Vault Vocabulary

> The canonical types and edge fields that define this vault's knowledge graph. This is the human-readable reference; the machine-readable source of truth is `scripts/kg/vault-ontology.ttl`.

---

## Note Types

Every note must have a `type:` field in frontmatter. Use one of these canonical values:

| Category | Type | Used in | Description |
|----------|------|---------|-------------|
| **Knowledge** | `theory-note` | 03 - Resources/[topic]/Theory/ | Theoretical framework or model |
| | `concept-note` | 03 - Resources/[topic]/Core Concepts/ | Named concept, idea, or pattern |
| | `method-note` | 03 - Resources/[topic]/Methods/ | Technique, procedure, how-to |
| | `finding` | 03 - Resources/[topic]/Findings/ | Experimental result, evidence |
| | `implementation-note` | 03 - Resources/[topic]/Implementation/ | Code repo, system build |
| **Literature** | `literature-note` | 03 - Resources/Literature/ | Paper, study, article |
| | `book-note` | 03 - Resources/Literature/ | Book or book-length work |
| | `author-note` | 03 - Resources/People/ | Researcher, writer, thought leader |
| **Entity** | `person` | 03 - Resources/People/ | Collaborator, contact |
| | `organization` | 03 - Resources/People/Organizations/ | Institution, lab, company |
| **External** | `external-resource` | 03 - Resources/[topic]/External Resources/ | Blog post, tool review, web content |
| | `tool` | 03 - Resources/External Resources/Tools & Repos/ | Software tool, application |
| **Navigation** | `moc` | 03 - Resources/[topic]/ | Map of Content — topic hub |
| | `index` | Various | Sub-index (e.g., LITERATURE-INDEX) |
| **Area** | `area` | 02 - Areas of Focus/ | Area of focus (Pullein) |
| **Project** | `project` | 01 - Projects/ | Time-bound effort serving an area |
| | `plan` | 01 - Projects/[project]/ | Implementation plan (PLAN.md) |
| | `decision` | 01 - Projects/[project]/ | Decision record |
| **Reference** | `reference` | 03 - Resources/Obsidian Reference/ | How-to, specification, standard |
| | `workflow` | 03 - Resources/Obsidian Reference/ | Documented process |
| | `course-notes` | 03 - Resources/Courses & Learning/ | Course or tutorial notes |
| **Other** | `fleeting-note` | 05 - Watching/ | Monitored item, quick thought |

### Literature Subtypes

Literature notes use `type: literature-note` with an optional `literatureType:` for granularity:

`research-paper`, `empirical-study`, `position-paper`, `benchmark-paper`, `working-paper`, `perspective`, `modeling-study`, `randomized-controlled-trial`, `industry-report`, `dissertation`, `comment`, `blog-research`

---

## Edge Fields

Frontmatter fields that create typed relationships in the knowledge graph. Each maps to an RDF property via `scripts/kg/vault-context.jsonld`.

| Field | Meaning | Source types → Target types |
|-------|---------|---------------------------|
| `up:` | Parent in hierarchy | Any → MOC, index |
| `area:` | Area of focus served | Project, MOC → area |
| `concept:` | Concept discussed | Literature, implementation → concept, theory, method |
| `implementation:` | Code implementing this | Concept, theory → implementation |
| `source:` | Literature source | Any → literature, book |
| `extends:` | Builds upon | Theory, concept → theory, concept |
| `criticizes:` | Challenges/opposes | Any → any (intellectual disagreement) |
| `supports:` | Validates/agrees | Any → any (intellectual support) |
| `related:` | Lateral connection | Any → any (catch-all, prefer specific fields) |
| `author:` | Person who authored | Literature, book, external-resource → author-note |
| `affiliation:` | Org membership | Person, author → organization |
| `collaborator:` | Project collaborator | Project → person |

### Domain/Range Guidance

- `concept:` should point to concept-note, theory-note, or method-note — NOT to a MOC (use `up:` for hierarchy)
- `source:` should point to literature-note or book-note — NOT to external-resource
- `extends:` targets should be the same category as the source (theory extends theory, concept extends concept)
- `implementation:` should point to implementation-note — NOT to concept-note

---

## Curator Observation Fields (optional)

When the ontology fit is uncertain, note-creation skills can flag for review:

| Field | Purpose |
|-------|---------|
| `curator_status:` | `pending` / `reviewed` / `accepted` / `declined` |
| `curator_suggested_type:` | Suggests a better type |
| `curator_suggested_up:` | Suggests a better parent |
| `curator_observations:` | Free-text reasoning |

The `/curator` skill harvests notes with `curator_status: pending`.

---

## Deprecation Notes

If you encounter these in notes, fix them on contact:

| Old | New |
|-----|-----|
| `noteType:` | `type:` |
| `relatedConcepts:` | `concept:` (edge field) |
| `relatedLiterature:` | `source:` (edge field) |
| `implementations:` | `implementation:` (edge field) |
