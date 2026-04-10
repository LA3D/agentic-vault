---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - architecture
---

# Vault Architecture

> How this vault is organized, why it's structured this way, and how the pieces work together.

---

## Design Principles

1. **Areas are the foundation** — everything connects back to an area of focus (Pullein/GAPRA)
2. **Progressive disclosure** — navigate in layers, never read everything at once
3. **Typed notes with typed relationships** — frontmatter edge fields create a queryable knowledge graph
4. **Agent-native** — structured for Claude Code to navigate, create, and maintain
5. **Two masters** — templates and structure serve both human (Obsidian UI) and agent (Claude Code)
6. **Local-first** — plain markdown on disk, git for versioning, no cloud database

---

## Folder Structure

```
/
├── VAULT-INDEX.md              # Top-level routing table
├── CLAUDE.md                   # Claude Code's orientation guide
├── .claude/
│   ├── rules/                  # Always-loaded behavioral rules (7 files)
│   ├── skills/                 # On-demand capabilities (invoked via /skill-name)
│   ├── settings.json           # Hooks and configuration
│   └── agent-memory/           # Persistent memory for skill subagents
│
├── 02 - Areas of Focus/        # THE FOUNDATION — your 6-8 life areas
│   ├── Research & Scholarship.md
│   ├── Health & Wellness.md
│   └── ...                     # Created during onboarding
│
├── 01 - Projects/              # Time-bound efforts serving areas
│   ├── Project Name.md         # Project overview + tasks
│   └── Project Name/           # Sub-notes: PLAN.md, decisions, etc.
│
├── 03 - Resources/             # Knowledge organized by topic
│   ├── Literature/             # Paper notes (@author-year-keyword.md)
│   │   └── LITERATURE-INDEX.md # Exhaustive catalog by topic
│   ├── Obsidian Reference/     # How-the-vault-works docs (you're reading one)
│   ├── People/                 # Author notes, person notes
│   │   └── Organizations/      # Institution notes
│   └── [Your Topics]/          # Created as your vault grows
│       ├── [Topic] MOC.md      # Map of Content — navigation hub
│       ├── Core Concepts/      # Concept and theory notes
│       ├── Theory/             # Theory notes
│       ├── Methods/            # Method notes
│       ├── Implementation/     # Code/experiment notes
│       └── External Resources/ # Blog posts, tools, web content
│
├── 04 - Archive/               # Completed or abandoned items
├── 05 - Watching/              # Fleeting notes — monitored but uncommitted
├── Daily/                      # Daily notes (YYYY-MM-DD.md)
├── Inbox/                      # Unsorted notes (processing queue, not storage)
├── Templates/                  # 7 note templates (human + agent use)
└── scripts/
    └── kg/                     # Knowledge graph pipeline
        ├── build-graph.sh      # Full pipeline: YAML → JSON-LD → Turtle → SHACL
        ├── vault-to-jsonld.py  # Frontmatter extraction
        ├── vault-context.jsonld # JSON-LD @context mapping
        ├── vault-ontology.ttl  # SKOS + RDFS vocabulary (source of truth)
        ├── vault-shapes.ttl    # SHACL validation + materialization rules
        ├── vault-queries.ttl   # Self-describing query catalog
        └── sparql/             # Standalone .rq query files
```

---

## The Three Memory Layers

This vault implements a cognitive architecture for Claude Code:

### 1. Working Memory (context window)
- **CLAUDE.md** + **7 rule files** loaded every session (~8K tokens)
- Provides behavioral guidance, not knowledge content
- The "orientation" layer — tells Claude how to work, not what to know

### 2. Procedural Memory (skills)
- **Skills** (`.claude/skills/`) — on-demand capabilities invoked by name
- Each skill is a detailed procedure: when to use it, how to execute, what to check
- Core skills handle vault mechanics (encode, retrieve, review, audit)
- Domain skills handle domain-specific decisions (installed as your work evolves)

### 3. Semantic Memory (the vault itself)
- **670+ typed notes** (as your vault grows) with frontmatter edge fields
- **16+ MOCs** organizing notes by topic
- **Knowledge graph** (Turtle/RDF) queryable via SPARQL
- Navigable via progressive disclosure: VAULT-INDEX → MOC → note

---

## How Claude Code Interacts with the Vault

### Reading (retrieval)
1. Progressive disclosure: VAULT-INDEX → MOC → target note
2. Text search: `obsidian search` (CLI, fast) or Grep (fallback)
3. Graph queries: SPARQL via `arq` for multi-hop traversal
4. Structured retrieval: `/retrieve` skill for budget-aware context loading

### Writing (encoding)
1. `/encode` pipeline: Router → Template → Write → Wire → Verify → Commit
2. Dynamic MOC discovery: Router scans for `*MOC.md` files, doesn't use hardcoded tables
3. Two-level wiring: MOC/index listing + reciprocal link discovery
4. Verification gate: every note is read back and checked before commit

### Maintaining (meta-cognition)
1. `/audit` — vault-wide structural health check
2. `/review-note` — single-note quality review with specialist agents
3. `/curator` — ontology governance, vocabulary evolution
4. `/session-retro` — end-of-session reflection and daily note update

---

## The Knowledge Graph Pipeline

Frontmatter edge fields are the vault's structured assertions. The KG pipeline makes them queryable:

```
YAML frontmatter  →  vault-to-jsonld.py  →  JSON-LD  →  riot  →  Turtle (RDF)
                                                                      ↓
                                            SHACL validation  ←  vault-shapes.ttl
                                                                      ↓
                                            SPARQL queries  ←  arq + vault-queries.ttl
```

**Dependencies**: Python 3, PyYAML, Apache Jena (arq, riot, shacl)
**Build**: `scripts/kg/build-graph.sh --stats`
**Query**: `arq --data=scripts/kg/vault-graph-full.ttl --query=scripts/kg/sparql/[query].rq`

---

## Cross-Repo Integration

This vault works alongside your code projects:

- **Vault-level planning** (`01 - Projects/PLAN.md`): Strategic — goals, research questions, area connections
- **Repo-level planning** (in git repos): Tactical — implementation, architecture
- **Bridge**: `claude --add-dir /path/to/vault` gives Claude access to vault knowledge while coding
- **Shell aliases**: Simplify the bridge pattern for daily use

---

## For Reference

- [[How Progressive Disclosure Works]] — navigation in layers
- [[How Wikilinks Create Structure]] — links as graph edges
- [[How the Index System Works]] — the routing hierarchy
- [[Vault Vocabulary]] — canonical types and edge fields
- [[Integration Ecosystem]] — external tool options and setup
- [[Areas of Focus - Pullein Methodology]] — the GAPRA framework
