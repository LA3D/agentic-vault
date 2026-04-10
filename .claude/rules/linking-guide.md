# Linking Guide

How to link projects, concepts, implementations, and daily work in this vault.

---

## Auto-Linking Workflow

When processing journal entries or new notes:
1. Identify entities (people, places, concepts, projects)
2. Search vault for existing notes on those entities
3. Add `[[wikilinks]]` throughout the document
4. Create new entity notes only if they don't already exist

---

## Linking Code Projects to Vault

> **Dev path**: Set during onboarding (see `owner-context.md`). Default convention: `~/dev/git/[organization]/[repo]/`

**Pattern**:
- **Project note** (`01 - Projects/`) → lists repos + links to concept notes
- **Implementation note** (`03 - Resources/.../Implementation/`) → links repo + concepts
- **Daily note** → links concept work + repo paths + literature

**Cross-repo bridge**: Use `claude --add-dir /path/to/vault` when working in a git repo so Claude can reference vault knowledge while implementing code.

---

## Wikilink Conventions

- Use `[[Note Title]]` format — **bare note titles only**
- **NEVER use relative paths** (`[[../folder/Note]]` or `[[../../folder/Note]]`) in wikilinks. Obsidian resolves bare titles vault-wide. Relative paths are fragile, break when files move, and create inconsistency. Use `[[Note Title]]` or `[[Note Title|display text]]` instead.
- If two notes share the same title (rare), disambiguate with the folder prefix: `[[folder/Note Title]]` — but prefer renaming one note to avoid the collision.
- Prefer bidirectional links over unlinked mentions
- Check existing notes before creating new ones
- Link from daily notes to concepts and projects
- Use frontmatter edge fields for typed relationships (see [typed-relationships.md](typed-relationships.md))

---

## Map of Content (MOC) Strategy

- Link all relevant notes in a domain
- Add "Agent Navigation Notes" section for session breadcrumbs (5-10 lines max)
- Place in appropriate PARA category
- List in VAULT-INDEX.md for discoverability

---

## Typed Relationships

Notes declare structured relationships via frontmatter edge fields. These drive the vault's knowledge graph (SPARQL-queryable via `scripts/kg/`) and Claude Code's navigation. See [typed-relationships.md](typed-relationships.md) for the full taxonomy.

**Templates** with edge field patterns:
- `Templates/Area of Focus.md` — `up:` (areas link to VAULT-INDEX)
- `Templates/Concept Note.md` — `up:`, `extends:`, `source:`, `implementation:`
- `Templates/Literature Note.md` — `concept:`, `supports:`, `criticizes:`, `source:`
- `Templates/Implementation Note.md` — `concept:`, `source:`
- `Templates/Project Note.md` — `area:`, `collaborator:`, `related:`

**Area connections**: When creating or editing projects and MOCs, populate `area:` to link them to the area of focus they serve. This is the Pullein "foundation" — every project and MOC should connect back to an area.

Use `type:` (not `noteType:`) for note typing. When editing existing notes, opportunistically add missing edge field properties and remove legacy fields (`relatedConcepts`, `relatedLiterature`, `implementations`).

---

**Related**:
- [typed-relationships.md](typed-relationships.md) — Full type taxonomy and edge fields
- [vault-navigation.md](vault-navigation.md) — Navigation patterns and health checks
