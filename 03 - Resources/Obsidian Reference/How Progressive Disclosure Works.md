---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - navigation
---

# How Progressive Disclosure Works

> Claude navigates this vault in layers — never reading all notes in a folder, always following links from general to specific.

---

## The Problem Progressive Disclosure Solves

A vault with hundreds of notes can't be searched effectively by reading everything. Grep finds text but not meaning. An LLM reading every file wastes context window on irrelevant content. Progressive disclosure solves this by organizing knowledge into layers that narrow progressively:

**Layer 1 — VAULT-INDEX.md** (~50 lines): A routing table. Points to areas, projects, and MOCs. Claude reads this first to orient. "Where should I look for information about topic X?"

**Layer 2 — Sub-indexes and MOCs** (~50-200 lines each): Domain-level maps. LITERATURE-INDEX catalogs all literature notes by topic. A MOC (Map of Content) organizes one domain's concept notes, theory notes, methods, and findings. "What do we know about topic X?"

**Layer 3 — Individual notes** (full detail): The actual knowledge — concept definitions, literature summaries, implementation details. Claude only reads these when it has a specific reason to.

---

## How Claude Uses This

When you ask "What do we know about topic X?", Claude doesn't grep the whole vault. Instead:

1. **Read VAULT-INDEX.md** → find which MOC or sub-index covers topic X
2. **Read that MOC** → find which specific notes discuss topic X
3. **Read those notes** → get the detail needed to answer

This is 3 reads instead of 300. The vault's structure does the filtering.

---

## How Wikilinks Enable This

Each layer points to the next via `[[wikilinks]]`. VAULT-INDEX has `[[Your Topic MOC]]`. The MOC has `[[Specific Concept Note]]`. The concept note has `[[Literature/@source-paper]]`. Claude follows these links like a researcher following citations — each hop narrows the focus.

See [[How Wikilinks Create Structure]] for more on how links form a traversable graph.

---

## How Frontmatter Edge Fields Add Structure

Beyond wikilinks in text, notes declare typed relationships in their YAML frontmatter:

```yaml
up: "[[Parent MOC]]"        # Where this note sits in the hierarchy
concept: "[[Key Concept]]"  # What concepts this discusses
source: "[[Source Paper]]"   # What literature supports this
extends: "[[Base Theory]]"  # What this builds upon
```

These edge fields are consumed by the KG pipeline (`scripts/kg/`) to build a queryable knowledge graph. Claude can ask "what literature supports concept X?" via SPARQL, rather than reading every literature note hoping to find a match.

See [[Vault Vocabulary]] for the full list of edge fields and their meanings.

---

## The Index Update Rule

Progressive disclosure only works if indexes are kept current. When you create a note:
- Add it to its parent MOC or sub-index
- This makes it *discoverable* from the upper layers
- An unindexed note is invisible to progressive disclosure — Claude can only find it via text search

The `/encode` skill handles this automatically. If creating notes manually, update the relevant MOC.

---

## For Vault Builders

**Keep VAULT-INDEX lean** — it's a routing table, not an exhaustive catalog. One line per MOC or project.

**MOCs are curated, not exhaustive** — organize notes by theme within a MOC, add "Agent Navigation Notes" for discovered paths.

**Create new MOCs as clusters emerge** — if you have 3+ notes on a topic with no MOC, the `/encode` skill will suggest creating one.
