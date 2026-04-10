# Vault Navigation

How Claude navigates and maintains this vault efficiently.

---

## Voice Input

If the vault owner uses speech-to-text for input, **always assume voice-to-text artifacts in user messages**: misheard words, missing punctuation, run-on sentences, filler words ("um", "uh"), homophones, and imprecise proper nouns. Interpret charitably — infer intent from context rather than treating dictation artifacts literally. When a spoken term doesn't match a vault note name exactly, try fuzzy matching before asking for clarification.

---

## CLI-First Principle

**Obsidian CLI** is built into Obsidian v1.12+ (not an npm package). It requires the Obsidian app to be running and communicates with it via local IPC. Registered via Settings > General > Command line interface.

**Prefer Obsidian CLI** over grep/Glob for vault content queries:

```bash
# Search vault content (uses pre-built index)
obsidian search query="TOPIC" limit=10

# Find backlinks to a note
obsidian backlinks file="Note Title"

# List outgoing links
obsidian links file="Note Title"

# Browse tags
obsidian tags sort=count counts

# Search by property
obsidian properties sort=count counts

# Read a note without opening it
obsidian read file="Note Title"

# Task management
obsidian tasks todo                          # All open tasks vault-wide
obsidian tasks todo path="01 - Projects"     # Project tasks only
obsidian task ref="path:line" done           # Mark complete via CLI
obsidian daily:read                          # Read today's daily note
obsidian daily:append content="- [ ] Task"   # Append to daily note
```

**For structural/graph queries**: Use the knowledge graph (SPARQL via `arq`) when the question is about how things *connect* across files — multi-hop relationships, concept chains, area rollups, hub detection. Grep/CLI answer *content* questions (what's in a file); the KG answers *topology* questions (what connects to what). Use the KG to discover WHERE to look, then file tools to read WHAT you found.

**For structured retrieval**: Use `/retrieve` when you need to pull multiple related notes into working memory with budget awareness. It returns a manifest (reading plan) instead of raw content, and supports three modes: targeted ("what do we know about X"), contextual ("what's relevant to this note"), and exploratory ("what connects to X that I haven't seen").

**Reserve grep/Glob for**: non-vault code searches, regex patterns, file type filtering outside the vault.

**If Obsidian is not running**: Fall back to grep/Glob. The CLI will return "command not found" or connection errors. Note this to the user — many vault operations are degraded without the app running.

---

## Progressive Disclosure Navigation

Navigate in layers — never read all notes in a folder:

1. **VAULT-INDEX.md** — Routing table. Points to areas, sub-indexes, and MOCs. Start here.
2. **Areas of Focus** (`02 - Areas of Focus/`) — The *why* layer. Foundational areas define what matters. Each links to its supporting MOCs, projects, and resources.
3. **Sub-indexes / MOCs** — Domain-level orientation (e.g., LITERATURE-INDEX, topic MOCs)
4. **Individual notes** — Full detail on a specific topic

**Pattern**: VAULT-INDEX → Area of Focus → MOC/Project → target note
**Shortcut**: VAULT-INDEX → MOC → target note (when the area is already known)

See `[[How Progressive Disclosure Works]]` for a detailed walkthrough.

---

## Structural Health Checks

Run after batch edits or at session start during vault maintenance:

```bash
# Find notes with no incoming links
obsidian orphans

# Find notes with no outgoing links
obsidian deadends

# Find wikilinks pointing to notes that don't exist
obsidian unresolved counts verbose
```

Report findings to the user. Orphans may need linking or archival. Unresolved links may indicate notes that should be created.

---

## Navigation Breadcrumbs

After navigating a topic area and discovering useful paths, add a brief **"Agent Navigation Notes"** section to the relevant MOC:

```markdown
## Agent Navigation Notes

- [Date]: Discovered that X connects to Y via Z
- Productive path: MOC → Concept → Implementation note → repo
- Tip: Search for "keyword" to find related external resources
```

Keep to 5-10 lines max. These accumulate across sessions to help future navigation.

---

## Vault Index Updates

- **Creating notes in areas with sub-indexes**: Update the sub-index (LITERATURE-INDEX, etc.), not VAULT-INDEX.md
- **Only update VAULT-INDEX.md** when: adding new MOCs, new projects, or top-level navigation changes
- Keep VAULT-INDEX.md as a routing table, not an exhaustive catalog

---

**Related**:
- [research-workflows.md](research-workflows.md) — Research session navigation patterns
- [linking-guide.md](linking-guide.md) — How to create connections between notes
- [typed-relationships.md](typed-relationships.md) — Type taxonomy and edge fields
