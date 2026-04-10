---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - navigation
  - indexing
---

# How the Index System Works

> The vault has a hierarchy of indexes that route Claude (and you) from the general to the specific. Understanding this hierarchy is key to keeping the vault navigable as it grows.

---

## The Hierarchy

```
VAULT-INDEX.md                    ← Top-level routing table (~50 lines)
├── Areas of Focus                ← The "why" — 8 foundational areas
├── Projects                      ← Active efforts serving areas
├── Sub-indexes                   ← Domain catalogs
│   ├── LITERATURE-INDEX.md       ← All literature notes, organized by topic
│   └── (others as vault grows)
└── MOCs (Maps of Content)        ← Topic-specific navigation hubs
    ├── [Your Topic] MOC.md
    └── [Another Topic] MOC.md
```

---

## What Each Level Does

### VAULT-INDEX.md
The top-level routing table. Lists areas, active projects, and MOCs. Claude reads this first every session to orient itself. Keep it lean — one line per entry, ~50 lines total.

**When to update**: When you create a new MOC, add a major project, or restructure areas.

### Sub-indexes (e.g., LITERATURE-INDEX.md)
Domain catalogs that list all notes of a specific type, organized by topic. LITERATURE-INDEX lists every literature note grouped by research area. These are more exhaustive than MOCs.

**When to update**: When you create a new note of that type. The `/encode` skill does this automatically.

### MOCs (Maps of Content)
Topic-specific navigation hubs. A MOC curates the most important notes on a topic, organizes them by subtopic, and provides context. Unlike sub-indexes (which aim to be exhaustive), MOCs are curated — they highlight the notes that matter most.

**Example structure** of a MOC:
```markdown
# [Your Topic] MOC

## Core Concepts
- [[Concept A]] — brief description
- [[Concept B]] — brief description

## Key Literature
- [[@smith-2025-example]] — what this showed
- [[@jones-2024-method]] — foundational method

## Implementation
- [[Project Implementation Note]] — what we built

## Agent Navigation Notes
- [Date]: Discovered that X connects to Y via Z
```

**When to create a new MOC**: When you have 3+ notes on a topic that aren't well-served by an existing MOC. The `/encode` skill will suggest this when it detects clustering.

**When to update**: When creating notes in that topic area. The `/encode` skill adds new notes to their parent MOC.

---

## The Update Rules

1. **Creating a literature note** → add to LITERATURE-INDEX.md under the right topic section
2. **Creating any other note** → add to its parent MOC (identified by the `up:` edge field)
3. **Creating a new MOC** → add to VAULT-INDEX.md
4. **Creating a new project** → add to VAULT-INDEX.md under Projects

The `/encode` skill handles rules 1-2 automatically. Rules 3-4 require awareness of the vault structure.

---

## Why This Matters for the Agent

An unindexed note is invisible to progressive disclosure. Claude navigates VAULT-INDEX → MOC → note. If the note isn't listed in a MOC, the only way to find it is text search — which works but bypasses the structured navigation path.

The discipline gate in `.claude/rules/discipline-gates.md` includes: "I'll update the MOC/index separately" as a universal rationalization — it never actually happens later. Update in the same session.

---

## For Vault Builders

- **VAULT-INDEX is a routing table, not a catalog** — keep it under 50 lines
- **MOCs are curated, sub-indexes are exhaustive** — different purposes
- **One MOC per topic area** — stored in `03 - Resources/[topic-folder]/[Topic] MOC.md`
- **Agent Navigation Notes** section in MOCs (5-10 lines max) — breadcrumbs from Claude's explorations that help future sessions navigate faster
