---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - navigation
  - wikilinks
---

# How Wikilinks Create Structure

> `[[Note Title]]` isn't just a hyperlink — it's a graph edge that Claude can traverse. The vault's structure emerges from the connections between notes.

---

## Two Types of Links

### 1. Body Wikilinks (narrative connections)

Links in the prose body of a note create navigable references:

```markdown
This concept builds on [[Parent Theory]] and was first described in
[[@smith-2025-example]]. See also [[Related Concept]] for an alternative approach.
```

Claude reads these and can "follow its nose" — when it encounters `[[Parent Theory]]`, it can read that note to get deeper context. Body links are informal, narrative, and bidirectional (Obsidian shows backlinks automatically).

### 2. Frontmatter Edge Fields (typed, queryable relationships)

YAML frontmatter declares structured relationships:

```yaml
---
type: concept-note
up: "[[Your Topic MOC]]"
extends: "[[Parent Theory]]"
source: "[[@smith-2025-example]]"
concept: "[[Related Concept]]"
---
```

These are consumed by the KG pipeline and become SPARQL-queryable. Claude can ask "what notes extend Parent Theory?" and get a precise answer without reading every file.

**Body links are for humans reading prose. Edge fields are for machines querying structure. Both matter.**

---

## How Claude Follows Links

When Claude encounters a wikilink — whether in body text or frontmatter — it can:

1. **Resolve it to a file**: `[[Note Title]]` → search for `Note Title.md` anywhere in the vault
2. **Read the target note**: Get the full content, including its own links and edge fields
3. **Follow those links recursively**: Navigate the graph to arbitrary depth

This is how progressive disclosure works in practice. VAULT-INDEX links to MOCs. MOCs link to concept notes. Concept notes link to literature. Literature links to other papers. Each hop adds specificity.

---

## Wikilink Conventions

- **Use bare titles**: `[[Note Title]]`, not `[[folder/Note Title]]`
  - Obsidian resolves bare titles vault-wide — no need for paths
  - Exception: disambiguate only when two notes share a title (rare)
- **Display text**: `[[Note Title|display text]]` for cleaner prose
- **Never use relative paths**: `[[../folder/Note]]` is fragile and breaks when files move
- **Check before creating**: Search the vault before creating a new note — duplicates fragment knowledge
- **Prefer bidirectional**: When Note A references Note B, check if Note B should reference Note A

---

## Links and the Knowledge Graph

When you run `scripts/kg/build-graph.sh`, the pipeline:

1. Reads every note's YAML frontmatter
2. Converts edge fields (`up:`, `concept:`, `source:`, etc.) to RDF triples via JSON-LD
3. Materializes implied relationships (if A extends B, then B is "extended by" A)
4. Produces a queryable Turtle file

Body wikilinks are NOT in the knowledge graph — only frontmatter edge fields. This is intentional: body links are informal and context-dependent, while edge fields are structured assertions about how knowledge connects.

---

## For Vault Builders

- When creating notes, think about what the note **relates to** — add both body links (for narrative flow) and edge fields (for graph structure)
- The `/encode` skill handles this automatically, suggesting edge fields based on content
- If you're linking to something that doesn't exist yet, that's OK — Obsidian tracks unresolved links, and you can create the target note later
