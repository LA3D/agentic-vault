---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - para
  - methodology
  - architecture
---

# Why PARA and How We Modify It

> This vault uses a modified PARA system as its organizational backbone. This note explains why PARA, what we changed, and how the vault's skills enforce the structure.

---

## What Is PARA?

PARA is Tiago Forte's organizational system for digital information. Four top-level categories:

- **P**rojects — time-bound efforts with a clear outcome
- **A**reas — ongoing responsibilities you maintain (no end date)
- **R**esources — reference material organized by topic
- **A**rchive — inactive items from the above three

The power of PARA is its simplicity: every piece of information goes in exactly one of four buckets, decided by a single question — *is this actionable?* Projects and Areas are actionable (you're doing something with them). Resources and Archive are reference (you might need them later).

---

## Why PARA for an Agentic Vault?

PARA works well for agent-assisted knowledge management because:

1. **Clear routing rules** — When Claude creates a note, PARA gives it an unambiguous destination. A project note goes in Projects. A concept note goes in Resources. No judgment calls about filing.

2. **Action-oriented hierarchy** — Areas → Projects → Tasks creates a natural priority chain. Claude can check "does this project serve an area?" as a quality gate.

3. **Archive as lifecycle** — Completed projects move to Archive, keeping the active workspace clean. Claude's `/audit` skill can detect stale projects.

4. **Progressive disclosure** — PARA's flat structure (4 top-level folders) maps naturally to the vault's layered navigation: VAULT-INDEX → PARA category → MOC → individual note.

---

## How This Vault Modifies PARA

Standard PARA has four folders. This vault has more, because we layer two systems:

### Pullein's Areas of Focus (the "why" layer)

Carl Pullein's GAPRA framework adds a hierarchy above PARA: **Areas → Goals → Projects → Actions → Resources**. The critical addition is making Areas the *foundation* — not just a filing cabinet, but the strategic layer that everything else serves.

In this vault, `02 - Areas of Focus/` contains your 6-8 life areas. Every project connects back to an area via the `area:` edge field. This connection is enforced by:
- The `/encode` Router (checks that projects have `area:` set)
- The `/audit` skill (flags projects missing area connections)
- SHACL shapes in the KG (validates `area:` edges at the graph level)

### Watching (the "not yet" layer)

Standard PARA has no place for items you're monitoring but haven't committed to — funding opportunities, emerging projects, ideas that need more thought. We add `05 - Watching/` for these fleeting notes. The rules:
- Use `type: fleeting-note` with `status: watching`
- When resolved: promote to `01 - Projects/` or archive to `04 - Archive/`
- **Inbox is NOT Watching** — Inbox is a processing queue (things arrive and get sorted), Watching is intentional monitoring

### Resources as Knowledge Graph

Standard PARA's Resources folder is flat — topics filed by subject. This vault adds structure:
- **MOCs** (Maps of Content) organize each topic area
- **Typed notes** (concept, theory, method, finding, implementation) classify knowledge
- **Edge fields** in frontmatter create queryable relationships
- **Sub-indexes** (LITERATURE-INDEX, etc.) provide exhaustive catalogs

This turns Resources from a filing cabinet into a navigable knowledge graph.

---

## The Folder Map

```
01 - Projects/              # PARA: Projects
│   ├── Project-Name.md     #   Project overview (type: project, area: [[Area]])
│   └── Project-Name/       #   Sub-notes: PLAN.md, decisions, meeting notes
│
02 - Areas of Focus/        # Pullein addition: the foundation
│   ├── Research & Scholarship.md
│   └── ...                 #   Each has goals, routines, review cadence
│
03 - Resources/             # PARA: Resources (enhanced with KG)
│   ├── Literature/         #   Literature notes + LITERATURE-INDEX
│   ├── People/             #   Author and person notes
│   ├── Obsidian Reference/ #   Vault documentation (you're reading one)
│   └── [Topic Folders]/    #   Each with a MOC + typed subfolders
│
04 - Archive/               # PARA: Archive
│                           #   Completed/abandoned projects, outdated resources
│
05 - Watching/              # Extension: monitored but uncommitted items
│                           #   type: fleeting-note, status: watching
│
Daily/                      # Daily notes — the work journal
Inbox/                      # Processing queue — sort then move, don't store
Templates/                  # Note templates for all types
```

---

## How the Router Enforces PARA

The `/encode` skill's Router determines where every new note goes. Its decision tree maps note types to PARA categories:

| Note type | PARA category | Location rule |
|-----------|--------------|---------------|
| `project`, `plan`, `decision` | **Projects** | `01 - Projects/` |
| `area` | **Areas** | `02 - Areas of Focus/` |
| `concept-note`, `theory-note`, `method-note`, `finding` | **Resources** | `03 - Resources/[MOC-folder]/[subfolder]/` |
| `literature-note`, `book-note` | **Resources** | `03 - Resources/Literature/` |
| `author-note`, `person`, `organization` | **Resources** | `03 - Resources/People/` |
| `external-resource`, `tool` | **Resources** | `03 - Resources/[MOC-folder]/External Resources/` or `03 - Resources/External Resources/Tools & Repos/` |
| `moc`, `index` | **Resources** | `03 - Resources/[topic]/` |
| `reference`, `workflow` | **Resources** | `03 - Resources/Obsidian Reference/` |
| `fleeting-note` | **Watching** | `05 - Watching/` |

The Router also has a **PARA-first check**: before consulting research MOCs, it asks whether the content belongs in the PARA structure at all. A note about a software tool you use is a `tool` note in External Resources, not a research concept in a MOC — even if the tool is AI-related.

### What the Router does when it can't find a home

1. **No matching MOC**: Asks you to create one, route to nearest, or place in Watching
2. **Ambiguous type**: Presents options and waits for your decision
3. **New topic area**: Suggests creating a MOC when 3+ notes cluster in an area without one

The Router discovers MOCs dynamically (scans for `*MOC.md` files) rather than using a hardcoded table, so it adapts as your vault grows.

---

## The Archive Lifecycle

Notes and projects flow through the PARA categories:

```
Idea → 05 - Watching/ (fleeting-note, monitoring)
         ↓ promote
      01 - Projects/ (active work)
         ↓ complete or abandon
      04 - Archive/ (preserved but out of the way)
```

Resources don't archive — they're permanent knowledge. But they do evolve: concept notes get refined, literature notes get updated with new connections, MOCs grow.

---

## For Reference

- [[Areas of Focus - Pullein Methodology]] — The GAPRA framework in detail
- [[Vault Architecture]] — Full structural reference
- [[How Progressive Disclosure Works]] — How PARA maps to navigation layers
- [[Vault Vocabulary]] — The type taxonomy that drives routing
