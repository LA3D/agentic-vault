---
name: encode
description: "Single authoritative note-creation pathway for all vault domains. Determines type, routes to correct location/MOC, populates frontmatter from templates, wires into MOC/indexes (with reciprocal links and 2-hop discovery), verifies, and commits. Use whenever creating a new note in the vault — 'create a note about X', 'new concept note', 'new literature note', 'encode this', 'save this to vault'. Also supports standalone wiring of existing notes — 'wire this note', 'connect this note', '/wire path/to/note.md'. Called programmatically by domain skills (process-readwise, readwise-book-processing, obsidian-knowledge-capture). Even if the user doesn't say 'encode', use this skill any time a conversation produces knowledge that should become a typed vault note, or when a note needs better connections."
---

# Encode

Single note-creation pathway for the vault. Every new note — concept, literature, external resource, author, fleeting thought — goes through Encode. Domain skills (Readwise processing, knowledge capture, research sessions) call Encode for the creation step and focus on their own domain-specific decisions.

---

## Interface

**Input** (from human or calling skill):

| Field | Required | Description |
|-------|----------|-------------|
| `content_description` | yes | What the note is about |
| `suggested_type` | no | Caller's best guess (validated against taxonomy) |
| `suggested_title` | no | Proposed title |
| `source_material` | no | URL, citekey, Readwise ID, or inline content |
| `extra_frontmatter` | no | Additional YAML fields to merge |
| `skip_commit` | no | `true` for batch operations (caller commits later) |

**Output**:

| Field | Description |
|-------|-------------|
| `note_path` | Path to created note |
| `note_type` | Canonical type assigned |
| `moc_updated` | Which MOC/index was updated |
| `curator_flagged` | Whether curator fields were added |

---

## Pipeline

### Step 1: Check for Existing Coverage

Before creating anything, search the vault:

```bash
obsidian search vault="obsidian" query="TOPIC_KEYWORDS" limit=10
```

If an existing note covers this topic:
- Tell the user: "Found [[Existing Note]] which covers this. Update it, or create a new note?"
- If updating: edit the existing note, skip Steps 2-5, jump to verification
- If creating: proceed (the new note should link to the existing one)

This prevents duplicate notes — the vault's biggest structural risk.

### Step 2: Route

**Express path**: If `suggested_type` is `fleeting-note` or the content is clearly a quick thought/reminder, skip the Router. Write directly to `05 - Watching/` with minimal frontmatter:

```yaml
---
type: fleeting-note
created: YYYY-MM-DD
status: watching
tags: [relevant-tags]
area: "[[Area if known]]"
---
```

No MOC update needed. Jump to Step 6 (verification).

**Standard path**: Read and follow the Router spec at `.claude/skills/encode/agents/router.md`. The Router has persistent memory at `.claude/agent-memory/encode-router/` — read `MEMORY.md` before making routing decisions.

The Router does five things in parallel:
1. **Validates type** against the canonical taxonomy (`.claude/rules/typed-relationships.md`)
2. **Determines domain** by querying text search, its own memory, and the KG
3. **Determines location** from type + MOC mapping
4. **Suggests connections** (2-5 typed edges)
5. **Assesses confidence** (high or low)

Pass to the Router: `content_description`, `suggested_type`, `suggested_title`, `source_material`, `extra_frontmatter`.

The Router returns: `type`, `title`, `location`, `moc`, `template`, `connections`, `confidence`, `confidence_reason`, `curator_flag`, `curator_observations`.

### Step 3: Confidence Gate

**High confidence** → Report the routing decision to the user in one line ("Creating concept-note in [Domain]/Core Concepts/, MOC: [Domain] MOC") and proceed.

**Low confidence** → Present the top 2-3 routing options:

```
This topic could go in multiple places:
1. concept-note → Your Topic MOC (memory architecture angle)
2. concept-note → [Another Domain] MOC (engineering practice angle)

Which fits better, or should I flag for curator review?
```

Wait for the human to choose. If the choice corrects the Router's top pick, update Router memory (`.claude/agent-memory/encode-router/MEMORY.md` → Routing Corrections section).

### Step 4: Create the Note

1. **Read the template** identified by the Router (see Router spec's Template Selection table for the full mapping). Override the template's `type:` field with the Router's determined type when they differ (e.g., `person` uses Person Note template but overrides `author-note` → `person`).

2. **Populate frontmatter**. Replace Templater placeholders (`<% ... %>`) with real values. Set:
   - `type:` from Router
   - `created:` today's date
   - Edge fields from Router's `connections` (use exact wikilink format: `"[[Note Title]]"`)
   - `status:` appropriate default (`emerging` for concepts, `unread` for literature, `active` for implementations)
   - Merge any `extra_frontmatter` from the caller
   - If Router set `curator_flag: true`, add curator observation fields

3. **Write the note body**. Use wikilinks to connect to existing vault notes. For concept/theory notes, prefer claim-form titles. Attribute claims to sources. Follow vault style (no AI-ese per `03 - Resources/context/ai_ese.md`).

4. **Write the file** using the Write tool to the Router's `location` path.

**Type-specific rules**:
- **literature-note**: Filename `@author-year-keyword.md`. Populate `authors:`, `year:`, `title:`, `venue:`, `citekey:`. Add `literatureType:` from the controlled vocabulary when determinable.
- **author-note**: Location `03 - Resources/People/`. Filename `lastname-firstname.md`. `up: "[[PEOPLE-INDEX]]"`. `aliases:` array is critical — include all name variants. Add `author:` edge on their literature notes.
- **organization**: Only create when referenced by 3+ existing notes.
- **external-resource / tool**: Include source URL. Body is 2-3 sentence summary, not full reproduction.

### Step 5: Wire (Post-Creation Integration)

Make the note discoverable and connected. This is where notes go from "created" to "wired into the knowledge graph."

#### 5.1: Update MOC/Index

Same as before — add the note to its parent:
- Literature notes → add to `03 - Resources/Literature/LITERATURE-INDEX.md` under the right topic section. To pick the section: read the `##` and `###` headings in LITERATURE-INDEX, match the paper's domain to the closest section. Key sections: "Memory Systems & Continual Learning", "Retrieval & RAG", "Tool Use", "Agent Infrastructure", "ML Foundations", "Knowledge Graphs & Ontologies", "FAIR Data", "AI & Society", "Decentralized Identity & Solid". If no section fits, add under the closest `##` heading or create a new `###` subsection.
- External resources → add to the appropriate EXTERNAL-INDEX.md for the domain
- Tool notes in `External Resources/Tools & Repos/` → add to `03 - Resources/External Resources/Tools & Repos/TOOLS-INDEX.md`
- All other types → add a wikilink entry to the MOC file identified by the Router
- Use Edit tool — add the wikilink in the appropriate section of the MOC/index
- Update sub-indexes if applicable: READWISE-INDEX for Readwise-sourced content. VAULT-INDEX only for major entry points.

#### 5.2: Reciprocal Link Discovery

Extract all outgoing typed edges from the new note's frontmatter (`related:`, `concept:`, `extends:`, `supports:`, `criticizes:`, `source:`). For each target wikilink:

1. Resolve to a file path (Glob for `**/<Target Title>.md`)
2. Read the target note's frontmatter and body
3. Check whether the target already mentions the new note
4. Classify into a tier:

| Edge Type | Reciprocal Action on Target | Why |
|-----------|----------------------------|-----|
| `related:` | **Auto-add** `related: "[[New Note]]"` to target's frontmatter | Symmetric by convention — both notes are equally lateral |
| `concept:` | **Auto-add** body wikilink `[[New Note]]` to concept note's "See also" section (or end of body) | Concept notes are hubs; adding discoverable links is their purpose |
| `supports:` / `criticizes:` / `extends:` | **Suggest only** — include in wiring report | Intellectual claims need human validation |
| `source:` | **No action** | Citation is one-directional; the KG materializes the inverse |

**Output**: two lists — `auto_reciprocal` (notes to modify) and `suggested_reciprocal` (notes to report).

#### 5.3: 2-Hop Connection Discovery

Find notes the Router didn't suggest but that connect to this note's concepts. Query two sources:

**SPARQL** — For each `concept:` target in the new note, run the 2-hop neighborhood query against `scripts/kg/vault-graph-full.ttl`:

```bash
arq --data="scripts/kg/vault-graph-full.ttl" --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT DISTINCT ?neighbor ?neighborTitle ?path WHERE {
  {
    ?neighbor vault:concept <CONCEPT_URI> .
    ?neighbor dcterms:title ?neighborTitle .
    BIND("shares concept" AS ?path)
  } UNION {
    <CONCEPT_URI> vault:conceptOf ?neighbor .
    ?neighbor dcterms:title ?neighborTitle .
    BIND("referenced by" AS ?path)
  } UNION {
    ?neighbor vault:extends <CONCEPT_URI> .
    ?neighbor dcterms:title ?neighborTitle .
    BIND("extends this" AS ?path)
  } UNION {
    ?neighbor vault:up ?moc .
    <CONCEPT_URI> vault:up ?moc .
    ?neighbor dcterms:title ?neighborTitle .
    BIND("sibling under MOC" AS ?path)
  }
  FILTER(?neighbor != <CONCEPT_URI>)
} LIMIT 15
SPARQL
)
```

Replace `<CONCEPT_URI>` with the note's graph URI. **Always resolve URIs by title lookup** rather than constructing them manually:
```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(echo 'PREFIX dcterms: <http://purl.org/dc/terms/> SELECT ?note WHERE { ?note dcterms:title "NOTE_TITLE" }')
```
URI slugification has edge cases (`@` in literature filenames, parent directory prefixes for Theory/Literature/etc.) that are easier to query than replicate. See the Retrieve skill's URI Resolution section for details.

**Text search** — `obsidian search vault="obsidian" query="NEW_NOTE_TITLE_KEYWORDS" limit=10` (or grep fallback).

**Merge**: Combine SPARQL and text results. Filter out notes already connected via frontmatter or already in `auto_reciprocal`/`suggested_reciprocal`. Rank by: shared concept count > same MOC > hub status.

**Output**: `discovery_candidates` — top 5 notes with connection path explanations.

#### 5.4: Reciprocal Link Execution

**For `related:` targets** (auto): Read target file. If `related:` array exists in frontmatter, append `"[[New Note Title]]"`. If no `related:` field, add one. Use Edit tool. Add modified file to the commit staging list.

**For `concept:` targets** (auto): Read target file body. Look for a "See also", "Related", or "Connections" section. If found, add `- [[New Note Title]]` as a list entry. If not found, append to end of body: `\n---\n\n## See Also\n\n- [[New Note Title]]`. Use Edit tool. Add modified file to the commit staging list.

**For suggested/discovery notes**: Do NOT modify. Include in the wiring report (Step 5.6).

#### 5.5: Discoverability Check

Count incoming links to the new note:

1. MOC/index listing (from Step 5.1): **+1**
2. Auto-added reciprocal `related:` edges (from Step 5.4): **+N**
3. Auto-added concept body wikilinks (from Step 5.4): **+N**
4. Pre-existing backlinks (check via `obsidian backlinks file="New Note Title"` or grep): **+N**

**Target**: ≥3 incoming links. This is advisory — report the score but don't block the commit. If under threshold, the wiring report will include suggestions for reaching it.

#### 5.6: Wiring Status Report

Print a structured report:

```
## Wiring Report: [Note Title]

**MOC updated**: [[MOC Name]] (section: [section name])
**Reciprocal links added** (auto):
  - [[Target A]] ← added related: [[New Note]]
  - [[Target B]] ← added related: [[New Note]]
  - [[Concept Note]] ← added body wikilink in See Also

**Reciprocal links suggested** (manual review):
  - [[Claim Note]] — new note supports this; consider adding supportedBy edge

**2-hop discovery candidates**:
  - [[Candidate A]] — shares concept [[X]] (sibling under MOC)
  - [[Candidate B]] — referenced by same concept

**Discoverability**: N/3 incoming links [✓ or ⚠ below threshold]
**Files modified**: [list of all files staged for commit]
```

### Step 6: Verification Gate

Read the note back and check every item. This is non-negotiable — a note that fails verification does not get committed.

- [ ] `type:` is populated with a canonical value from Vault Vocabulary
- [ ] `created:` date is set
- [ ] `up:` target exists (Read the MOC/index to confirm)
- [ ] All edge field targets exist (Glob check for each wikilink)
- [ ] Wikilinks in body text resolve to existing notes
- [ ] Note file is in the correct location per Router's routing table
- [ ] MOC/index has been updated with a link to this note
- [ ] No placeholder text remains (`[Topic]`, `TODO`, Templater syntax)
- [ ] If curator fields present, `curator_status: pending` is set
- [ ] Tags array is populated and relevant

**If ANY check fails**: Fix the issue and re-verify. Do not proceed to commit.

### Step 7: Commit and Rebuild

Unless `skip_commit` is true:

```bash
git add [note-file] [moc-or-index-file] [reciprocal-target-files...]
git commit -m "$(cat <<'EOF'
[Agent: Claude] Add [type]: [title]

- Created [path]
- Updated [MOC/index]
- Wired: N reciprocal links to [list of modified notes]
- Discoverability: N/3 incoming links

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

Then trigger a background KG rebuild:

```bash
scripts/kg/rebuild-async.sh
```

Run this with `run_in_background: true` — it takes ~6 seconds and shouldn't block the user.

---

## Calling Encode from Domain Skills

Domain skills delegate note creation to Encode. The pattern:

```
# In the domain skill's workflow:
# 1. Do domain-specific work (triage, classify, extract highlights, etc.)
# 2. Call Encode with the results:

Invoke /encode with:
  content_description: "Paper on CoT controllability by Chen et al. 2026..."
  suggested_type: literature-note
  suggested_title: "@chen-2026-cot-controllability"
  source_material: "readwise_book_id: 12345678"
  extra_frontmatter:
    readwise_book_id: 12345678
    literatureType: research-paper
  skip_commit: true  # batch mode — caller commits after all notes
```

The domain skill handles domain decisions (what's worth encoding, what type it probably is). Encode handles vault mechanics (routing, templating, wiring, verification).

---

## Discipline Gates

Apply all gates from `.claude/rules/discipline-gates.md` — especially the verification gate before committing and the "I'll add links later" rationalization. Every note needs a type, every note needs wiring, every note needs verification before commit.

## Batch Mode

When `skip_commit: true`, Encode creates the note and wires it but does NOT commit or trigger KG rebuild. The calling skill is responsible for:
1. Accumulating the list of files modified across multiple Encode calls (note files + MOC/index files + reciprocal targets)
2. Committing all files at once after the batch completes
3. Triggering one KG rebuild at the end (not per-note)

---

## Examples

### Concept Note (high confidence)

**User**: "Create a concept note about handle-first retrieval for agentic memory"

1. Search vault → no existing note on "handle-first retrieval"
2. Router: `concept-note` → `03 - Resources/[Domain]/Core Concepts/` → `[[Your Topic MOC]]` → high confidence
3. Read `Templates/Concept Note.md`, populate frontmatter:
   ```yaml
   type: concept-note
   up: "[[Your Topic MOC]]"
   extends: "[[Progressive Disclosure]]"
   source: "[[@zhang-2025-rlm]]"
   created: 2026-03-24
   status: emerging
   tags: [memory-architecture, retrieval]
   ```
4. Write to `03 - Resources/[Domain]/Core Concepts/Handle-First Retrieval Pattern.md`
5. Add wikilink to the domain MOC under Core Concepts section
6. Verify → all checks pass
7. Commit + background KG rebuild

### Cross-Domain Topic (low confidence)

**User**: "Create a note about agent evaluation frameworks that bridge memory and engineering"

1. Search vault → finds notes in both domains
2. Router: low confidence — topic straddles two MOCs
3. Present options: "This bridges [Domain A] and [Domain B]. Where should it live?"
4. User picks [Domain B] → proceed with that routing
5. Record correction in Router memory if it differed from Router's top pick
6. Create, wire, verify, commit

### Fleeting Note (express path)

**User**: "Quick thought — check if grant funding covers the new agent eval work"

1. Detect fleeting content → express path
2. Write to `05 - Watching/Grant Funding Agent Eval Coverage.md`:
   ```yaml
   type: fleeting-note
   created: 2026-03-24
   status: watching
   area: "[[Research & Scholarship]]"
   tags: [funding, follow-up]
   ```
3. No MOC update
4. Verify → passes
5. Commit

---

## Standalone Wire Mode

Wire can run on existing notes — not just newly created ones. Use this to retroactively connect notes that were created before the Wire pipeline existed, or to re-wire notes after the vault structure changes.

**Triggers**: `/wire path/to/note.md`, "wire this note", "connect this note to the vault", "rewire"

**Pipeline**:

1. Read the target note's frontmatter (extract `type`, `up`, `concept`, `related`, `extends`, `supports`, `criticizes`, `source`)
2. Verify MOC/index listing (Step 5.1) — add if missing
3. Run reciprocal link discovery (Step 5.2)
4. Run 2-hop connection discovery (Step 5.3)
5. Execute reciprocal links (Step 5.4)
6. Run discoverability check (Step 5.5)
7. Print wiring status report (Step 5.6)
8. Commit modified files:
   ```bash
   git add [target-note] [moc-if-modified] [reciprocal-target-files...]
   git commit -m "$(cat <<'EOF'
   [Agent: Claude] Wire: [note title]

   - N reciprocal links added
   - Discoverability: N/3 incoming links

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```
9. Trigger background KG rebuild

Standalone Wire skips Steps 1-4 of Encode (the note already exists). It reuses the same Wire substeps 5.1-5.6.

---

## Reference Files

| File | Role | When to read |
|------|------|-------------|
| `.claude/skills/encode/agents/router.md` | Router subagent spec | Always — spawned in Step 2 |
| `.claude/agent-memory/encode-router/MEMORY.md` | Router persistent memory | Router reads at start |
| `.claude/agent-memory/encode-router/moc-coverage.md` | Detailed MOC→topic map | Router reads for domain routing |
| `.claude/rules/typed-relationships.md` | Type taxonomy + edge fields | Router validates types |
| `03 - Resources/Obsidian Reference/Vault Vocabulary.md` | Domain/range constraints | Router validates edges |
| `Templates/*.md` | Note templates | Step 4 (apply template) |
| `scripts/kg/rebuild-async.sh` | Background KG rebuild | Step 7 (post-commit) |
