---
name: retrieve
description: "Structured retrieval of vault notes into working memory. Three modes: targeted ('what do we know about X'), contextual ('what's relevant to this note'), exploratory ('what connects to X that I haven't seen'). Returns reading plans with budget management, not raw file dumps. Use when loading vault context for research, synthesis, meeting prep, or any task that needs to pull relevant notes. Also use when: 'find related notes', 'pull context for X', 'explore connections to X', 'what connects to', 'show me what we have on'. Prefer this over ad-hoc obsidian search + Read when you need structured, budget-aware retrieval."
---

# Retrieve

Pull relevant vault notes into working memory. Returns a structured reading plan (manifest), not raw content. Three modes for different retrieval needs. Budget-aware — tracks how much context has been loaded and warns before exceeding thresholds.

**Why this exists**: Notes range from 1K to 190K tokens. Loading 5 theory notes naively consumes 50K+ tokens (25% of context). Retrieve gives you a manifest first, so you can decide what's worth loading before committing context budget.

---

## Mode Detection

Classify the query into one of three modes:

| Signal | Mode |
|--------|------|
| "What do we know about X?", "find notes about X", "what's in the vault on X" | **Targeted** |
| "What's relevant to [[Note]]?", "context for this paper", "related to this note" | **Contextual** |
| "What connects to X that I haven't seen?", "explore connections", "what am I missing" | **Exploratory** |

If unclear, default to **Targeted**.

---

## Step 0: Graph Freshness Check

### Running Named Queries

This skill references named queries from `scripts/kg/vault-queries.ttl` (e.g., `vq:concept-neighborhood`). To run one: Read the TTL file, find the `vq:<name>` block, extract the `sh:select` value, replace placeholders (e.g., `CONCEPT_SUBSTRING`, `NOTE_URI`), and pass to arq via process substitution. If the graph is unavailable, fall back to text search (`obsidian search` or grep). If arq fails, report the error and fall back.

### Graph Freshness

Before running SPARQL queries, verify the graph is current:

```bash
stat -f "%Sm" scripts/kg/vault-graph-full.ttl
```

If the graph is older than the most recent git commit (or older than 1 hour), trigger a rebuild:

```bash
scripts/kg/rebuild-async.sh
```

While the rebuild runs in the background (~6s), proceed with text search (`obsidian search` or grep). Use SPARQL results when they arrive. If the graph doesn't exist at all, fall back entirely to text search.

**Consistency note**: Audit *waits* for the rebuild (it needs accurate structural counts). Retrieve *proceeds* without waiting (it can supplement SPARQL with text search). This asymmetry is intentional — Audit needs precision, Retrieve needs responsiveness.

---

## Targeted Mode

**Intent**: "What do we know about X?" — find all notes about a topic.

### Pipeline

1. **SPARQL title search** — find notes whose title matches the topic:
   ```bash
   arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
   PREFIX vault: <https://example.com/vault/ontology#>
   PREFIX dcterms: <http://purl.org/dc/terms/>
   SELECT ?note ?title ?type ?pred ?targetTitle WHERE {
       ?note dcterms:title ?title .
       FILTER(CONTAINS(LCASE(?title), LCASE("TOPIC")))
       ?note a ?type .
       OPTIONAL {
           ?note ?pred ?target .
           ?target dcterms:title ?targetTitle .
           FILTER(?pred NOT IN (dcterms:title))
       }
   } ORDER BY ?title ?pred
   SPARQL
   )
   ```

2. **SPARQL concept neighborhood** — find notes connected to matching concepts (uses `vq:concept-neighborhood` from `scripts/kg/vault-queries.ttl`).

3. **Text search** — `obsidian search vault="obsidian" query="TOPIC" limit=15` (or grep fallback). Catches body-text mentions that SPARQL misses.

4. **Merge and rank**: Deduplicate by title. Rank by:
   - **Tier 1**: Concept/theory notes about the topic (they synthesize)
   - **Tier 2**: Method/finding notes (they provide evidence)
   - **Tier 3**: Literature notes referencing the topic
   - **Tier 4**: External resources mentioning it

5. **Build manifest** (see Manifest Format below). Cap at 20 entries.

---

## Contextual Mode

**Intent**: "What's relevant to this note?" — find the neighborhood of a specific note.

### Pipeline

1. **Read the anchor note's frontmatter** — extract `concept:`, `source:`, `extends:`, `supports:`, `criticizes:`, `related:` edges.

2. **Resolve anchor URI** — look up the note's title in the graph to get its URI:
   ```bash
   arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
   PREFIX dcterms: <http://purl.org/dc/terms/>
   SELECT ?note WHERE {
       ?note dcterms:title "ANCHOR_TITLE"
   }
   SPARQL
   )
   ```

3. **SPARQL note-neighborhood** — full 2-hop query (uses `vq:note-neighborhood` from `scripts/kg/vault-queries.ttl`). Replace `NOTE_URI` with the resolved URI.

4. **Rank**: Direct edges (1-hop) first, shared-concept notes (2-hop) second. Within each tier, rank by type relevance (concept > theory > literature > external).

5. **Sparse results fallback**: If SPARQL returns fewer than 8 notes (common for notes with few typed edges), supplement with text search: `obsidian search vault="obsidian" query="ANCHOR_TITLE_KEYWORDS" limit=15`. Merge with SPARQL results, deduplicating by title.

6. **Build manifest**. Cap at 20 entries.

---

## Exploratory Mode

**Intent**: "What connects to X that I haven't seen?" — discovery through graph traversal.

### Pipeline

1. **Resolve anchor URI** (same as Contextual Step 2).

2. **Cold neighbors** — SPARQL for underexplored notes in the neighborhood (uses `vq:cold-neighbors`). These are notes with <5 inbound edges — connected but not well-known.

3. **Cross-MOC bridges** — SPARQL for notes in other MOCs that reference this note's MOC (uses `vq:cross-moc-bridges`). These reveal unexpected connections across domains.

4. **Dangling concepts** — check the anchor's neighborhood for edge targets that have no `rdf:type` (they're referenced but don't exist as notes). These are knowledge gaps worth filling:
   ```bash
   arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
   PREFIX vault: <https://example.com/vault/ontology#>
   PREFIX dcterms: <http://purl.org/dc/terms/>
   SELECT DISTINCT ?target WHERE {
       <NOTE_URI> ?pred ?target .
       FILTER(?pred IN (vault:concept, vault:related, vault:extends))
       FILTER(isIRI(?target))
       FILTER NOT EXISTS { ?target a ?type }
   }
   SPARQL
   )
   ```

5. **Build manifest** with annotations: each entry tagged as "cold node", "cross-MOC bridge", or "missing concept". Cap at 15 entries.

---

## Manifest Format

Retrieve always returns a manifest — a structured reading plan, not raw content.

```
## Retrieval Manifest: [query description]

**Mode**: Targeted | Contextual | Exploratory
**Graph**: vault-graph-full.ttl (built [timestamp])
**Results**: N notes found, showing top M

| # | Title | Type | Connection | Size | Reason |
|---|-------|------|-----------|------|--------|
| 1 | [[Procedural Memory]] | concept-note | direct match | 8.6K | Primary concept note — synthesizes the topic |
| 2 | [[Wake-Sleep Memory Consolidation]] | theory-note | extends | 12.1K | Theory that builds on procedural memory |
| 3 | [[@chang-2026-karl]] | literature-note | references concept | 3.2K | Key paper — KARL agent with procedural memory |
| ... | | | | | |

**Budget**: 0 / 40K tokens loaded (0%)

### Reading Order

1. Start with **[[Procedural Memory]]** — the concept note gives the overview
2. If researching consolidation, read **[[Wake-Sleep Memory Consolidation]]** next
3. For specific implementations, pick from the literature notes by relevance
```

### Size Estimation

For the Size column, use file size as a proxy:
```bash
wc -c < "path/to/note.md"
```

Token estimate: bytes / 3 (conservative). A 9K byte note ≈ 3K tokens.

---

## Progressive Loading

After presenting the manifest, the agent (or user) requests content at increasing detail:

**Level 0 → Level 1**: "Show me the frontmatter for #1 and #3"
- Read only the YAML frontmatter block (type, edges, tags, status)
- ~200-500 tokens per note
- Reveals structural position without loading body

**Level 1 → Level 2**: "Load #1 fully"
- Full Read of the note
- Update budget tracker: `Budget: 8.6K / 40K tokens loaded (21%)`

**Budget warning**: When cumulative loaded tokens exceed 40K (20% of context), warn:
> "Working memory at 21% capacity (42K / 200K tokens). Loading more notes will reduce space for reasoning. Continue?"

This is advisory — don't block, just inform.

---

## URI Resolution

SPARQL queries require note URIs. The vault uses this URI scheme:

- **Base**: `https://example.com/vault/notes/`
- **Slug**: filename stem with spaces → hyphens, case preserved
- **Parent prefix**: notes in `{Literature, Theory, Implementation, External Resources, Methods, Memory Architecture, Findings}` get `ParentDir/` prepended

To find a note's URI, query by title:
```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(echo 'PREFIX dcterms: <http://purl.org/dc/terms/> SELECT ?note WHERE { ?note dcterms:title "NOTE_TITLE" }')
```

**Important**: Always resolve URIs by title lookup rather than constructing them manually. The slugification has edge cases (`@` in literature note filenames, triple hyphens from ` - ` separators) that are easier to query than to replicate.

---

## When NOT to Use Retrieve

- **Single known note**: If you know exactly which note you need, just Read it directly
- **Quick search**: `obsidian search` is faster for "does a note about X exist?"
- **Raw SPARQL**: Use `/vault-kg` when you need a custom query not covered by the retrieval modes
- **Transient context**: Health updates, daily note entries, task status → use memory files and daily notes, not Retrieve

---

## Reference Files

| File | Role | When to read |
|------|------|-------------|
| `scripts/kg/vault-queries.ttl` | SPARQL query catalog (41 queries) | To find or customize queries |
| `scripts/kg/vault-graph-full.ttl` | Materialized RDF graph | Data source for all SPARQL queries |
| `scripts/kg/rebuild-async.sh` | Background graph rebuild | When graph is stale |
| `.claude/rules/vault-navigation.md` | Progressive disclosure protocol | For navigation context |
| `.claude/skills/vault-kg/SKILL.md` | Raw SPARQL execution patterns | For custom queries beyond retrieval modes |
