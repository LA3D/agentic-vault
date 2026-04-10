---
name: memory-audit
description: "Audit .claude/memory/ files for misplaced content and adequate coverage. Classifies files as POINTER/OPERATIONAL/FEEDBACK/KNOWLEDGE/HYBRID. Four modes: standalone (/memory-audit) audits all files, session (/memory-audit session) checks modified files, compress (/memory-audit compress) shrinks oversized files, coverage (/memory-audit coverage) tests whether high-frequency prompts are served by current memory. Use when: 'memory audit', 'check memory files', 'what's in memory', 'memory health', 'drain memory', 'compress memory', 'did we over-prune', or 'memory coverage check'. Does NOT modify files — proposals require user approval."
---

# Memory Audit

Classify `.claude/memory/` files, detect misplacements, and propose routing corrections. This is the "drain" for the gravity problem: knowledge flows downhill into memory when it should land in the vault or rules.

**Principle**: Memory-audit flags, it doesn't fix. The report is advisory — the user decides what to act on.

**Anti-overpruning gate**: After any drain or compress operation, run `/memory-audit coverage` to verify high-frequency access patterns are still served. Memory exists for speed — if a common prompt now requires a vault Read, the pruning went too far. Memory and vault are complementary layers, not either/or: vault notes hold the structured knowledge, memory holds the operational quick-ref for things the agent needs every session.

**Feedback files are behavioral guardrails, not data.** Memory files aren't just information the agent can look up — they're context that shapes how the agent acts. A feedback correction in memory gets loaded into the context window and actively influences behavior. The same correction in a vault note would require the agent to think to look it up *before* making the mistake — which it won't, because the mistake is the default behavior the correction exists to override.

**Pruning rules for feedback files:**
1. **NEVER delete a feedback file unless the correction is provably encoded in a rule (`.claude/rules/`) or skill spec that loads automatically.** A vault note is NOT sufficient — vault notes require explicit Read calls.
2. **To verify graduation**: grep for the correction's key concept in `.claude/rules/*.md` and the relevant skill SKILL.md files. If found in text that loads every session, the feedback has graduated. If only found in a vault note or a skill that loads on demand, the feedback has NOT graduated — keep it.
3. **When in doubt, keep the feedback file.** The cost of a redundant 15-line file is negligible. The cost of losing a behavioral correction is repeated mistakes across sessions.

---

## Mode Detection

| Signal | Mode |
|--------|------|
| `/memory-audit`, "check memory", "what's in memory", "memory health" | **Standalone** (all files) |
| `/memory-audit session`, at session end via session-retro | **Session** (git diff scoped) |
| `/memory-audit compress`, "compress memory", "slim memory files" | **Compress** (oversized files) |

---

## Classification System

Every memory file gets one classification:

| Category | Signal | Correct Action |
|----------|--------|---------------|
| **POINTER** | Mostly links to vault/rules content; <30 lines; no unique knowledge | Check freshness -> delete if redundant |
| **OPERATIONAL** | Transient state (dates, "right now" phrasing, changes daily/weekly) | Leave in memory — correct location |
| **FEEDBACK** | Behavioral corrections ("don't do X", "Why:", "How to apply:"); <50 lines | **Keep unless provably graduated to a rule or always-loaded skill spec.** Vault notes don't count — they require explicit lookup. See anti-overpruning gate. |
| **KNOWLEDGE** | Substantial reference (people, tools, workflows); >50 lines; rarely changes; could be a vault note | Promote to vault via `/encode` -> replace with pointer |
| **HYBRID** | Mix of operational + knowledge; some sections change, others are stable | Extract knowledge -> vault; prune operational remainder |

---

## Standalone Mode (`/memory-audit`)

Full audit of all memory files. Run at session start for maintenance, or on demand.

### Step 1: Inventory

```bash
# List all memory files with sizes
# Set MEMORY_DIR to the project memory directory path
MEMORY_DIR="<memory-path>"
for f in "$MEMORY_DIR"/*.md; do
  [ "$f" = "$MEMORY_DIR/MEMORY.md" ] && continue  # skip index
  LINES=$(wc -l < "$f")
  BYTES=$(wc -c < "$f")
  AGE=$(git log -1 --format="%ar" -- "$f" 2>/dev/null || echo "unknown")
  echo "$(basename $f): ${LINES} lines, ${BYTES} bytes, modified $AGE"
done
```

### Step 2: Classify Each File

Read each file and apply classification heuristics:

1. **Read frontmatter** — check `type:` field (user, feedback, reference, project)
2. **Check content signals**:
   - File is mostly wikilinks/pointers with no unique content? -> POINTER
   - Contains dates, current status, "right now" language? -> OPERATIONAL
   - Contains "Why:", "How to apply:", correction language? -> FEEDBACK
   - Contains structured reference (CLI commands, people, workflows), >50 lines, stable? -> KNOWLEDGE
   - Mix of the above? -> HYBRID
3. **Record confidence**: high (clear signals) or low (ambiguous — flag for human review)

### Step 3: Check Freshness

For each file:
```bash
git log -1 --format="%ar %H" -- "$MEMORY_DIR/filename.md"
```

- POINTER files not modified in >30 days -> strong delete candidate
- KNOWLEDGE files not modified in >14 days -> stable enough to promote
- OPERATIONAL files not modified in >7 days -> may be stale (flag)

### Step 4: Check Redundancy

For POINTER and KNOWLEDGE files, search for vault coverage:

```bash
obsidian search vault="obsidian" query="TOPIC_KEYWORDS" limit=5
```

Also check `.claude/rules/` for overlap:
```bash
grep -l "KEYWORD" .claude/rules/*.md
```

If vault/rules coverage is complete, flag as redundant.

### Step 5: Check Graduation (FEEDBACK only)

For each FEEDBACK file, search for the correction topic in:
1. `.claude/rules/*.md` — behavioral rules
2. `.claude/skills/encode/agents/router.md` — Router spec
3. `.claude/agent-memory/encode-router/MEMORY.md` — Router persistent memory
4. Relevant skill specs (if the feedback is domain-specific)

If the correction is explicitly encoded in rules/skills, flag as graduated.

### Step 6: Check Bloat

Flag files exceeding thresholds:

| Category | Threshold | Action |
|----------|-----------|--------|
| OPERATIONAL | >100 lines or >10KB | Suggest compression |
| FEEDBACK | >50 lines or >5KB | Suggest extraction to rule/skill |
| HYBRID | >150 lines | Suggest extraction + compression |
| Any file | >200 lines | Mandatory review |

### Step 7: Check MEMORY.md Index Drift

Compare the topic file table in MEMORY.md against actual files on disk:
- Files in MEMORY.md table that don't exist -> **Error** (stale pointer)
- Files on disk not in MEMORY.md table -> **Warning** (undiscoverable)
- Descriptions that don't match current content -> **Info** (drift)

### Step 8: Report

```
## Memory Audit Report — YYYY-MM-DD

### Summary
| Metric | Value |
|--------|-------|
| Total files | N (excluding MEMORY.md) |
| Total lines | N |
| POINTER | N (N stale, N redundant) |
| OPERATIONAL | N (N oversized) |
| FEEDBACK | N (N graduated) |
| KNOWLEDGE | N |
| HYBRID | N |

### Proposed Actions (priority order)

**Delete** (redundant/stale POINTER files):
1. `filename.md` — N lines, redundant with [vault note or rule]

**Promote** (KNOWLEDGE -> vault via /encode):
1. `filename.md` — N lines -> [proposed vault type and location]

**Extract + Slim** (HYBRID):
1. `filename.md` — N lines -> extract [section] to vault, target N lines

**Archive** (graduated FEEDBACK):
1. `filename.md` — correction absorbed into [rule/skill]

**Compress** (oversized):
1. `filename.md` — N lines, threshold N, target N lines

### MEMORY.md Index Drift
- [Files in table but not on disk]
- [Files on disk but not in table]
```

---

## Session Mode (`/memory-audit session`)

Lightweight — checks only memory files modified this session.

### Step 1: Scope

```bash
# Set MEMORY_DIR to the project memory directory path
MEMORY_DIR="<memory-path>"
# Files modified since session start (today's first commit or HEAD~5)
SESSION_START=$(git log --since="today 00:00" --reverse --format="%H" | head -1)
git diff --name-only ${SESSION_START:-HEAD~5} -- "$MEMORY_DIR/*.md"
```

If no memory files were modified, report "No memory changes this session" and exit.

### Step 2: Per-File Check

For each modified file, run Steps 2-6 from standalone mode.

### Step 3: Session Report

Compact version of the standalone report — just the modified files with classifications and proposals.

---

## Compress Mode (`/memory-audit compress`)

For files flagged as oversized. Produces a compressed version for user approval.

### Pipeline

1. Read the file and classify each section:
   - **Active state** (changes session-to-session) -> keep
   - **Completed details** (historical, captured in vault) -> prune
   - **Knowledge reference** (stable, should be in vault) -> extract first, then prune
   - **Pointer** (links to vault notes) -> keep (compact)

2. Produce compressed version with target sizes:
   - OPERATIONAL: <50 lines
   - FEEDBACK: <30 lines
   - HYBRID: <80 lines after extraction

3. Present the before/after diff to the user for approval before overwriting.

### Size Triggers

| Current Size | Action |
|-------------|--------|
| >100 lines | Suggest compression |
| >200 lines | Strongly recommend compression |
| >10KB | Mandatory review |

---

## Coverage Mode (`/memory-audit coverage`)

Test whether high-frequency access patterns are served by current memory. Prevents over-pruning.

### Principle

Memory exists for speed. If a common prompt requires a vault Read to answer, the memory is under-provisioned. The test: can the agent handle these prompts using ONLY what's loaded in MEMORY.md + topic files, without reading vault notes?

### Deriving High-Frequency Patterns

Don't guess — measure from two sources.

**Source 1: Trajectory files** (most accurate). Claude Code writes JSONL session logs to `.claude/projects/<project>/`. Extract Read tool calls to find which files the agent actually accesses most:

```bash
python3 << 'PYEOF'
import json, collections, os, glob
vault_dir = "<your-project-dir>"
files = sorted(
    [f for f in glob.glob(f"{vault_dir}/*.jsonl") if os.path.getsize(f) > 10000],
    key=os.path.getmtime, reverse=True
)[:10]
file_reads = collections.Counter()
for fpath in files:
    with open(fpath) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except: continue
            if obj.get('type') == 'assistant':
                for block in (obj.get('message',{}).get('content',[]) or []):
                    if isinstance(block, dict) and block.get('type') == 'tool_use' and block.get('name') == 'Read':
                        fp = block.get('input',{}).get('file_path','')
                        if fp: file_reads[fp.split('obsidian/')[-1]] += 1
for f, c in file_reads.most_common(20):
    print(f"  {c:3d}x  {f}")
PYEOF
```

Files read 3+ times across 10 sessions = empirically high-frequency.

**Source 2: Daily note wikilinks** (backup). Scan for recurring entities across sessions:

```bash
for f in $(ls -t Daily/*.md | head -10); do
  grep -o '\[\[[^]]*\]\]' "$f" 2>/dev/null
done | sort | uniq -c | sort -rn | head -20
```

**Empirical high-frequency categories** (validate from your own trajectory scans):
- Active project notes and their plans (PLAN.md, [Topic] MOCs, active projects)
- Active project memory state (example-project.md, team-contacts.md)
- Navigation indexes (LITERATURE-INDEX, READWISE-INDEX)
- Skill specs for frequently-invoked skills (encode, vault-curator)
- Operational state (current-situation.md, tool-setup.md)

**Typically NOT high-frequency** (vault lookup is fine):
- Research authors and their papers (read 1x when processing, not revisited)
- Specific concept/theory notes (accessed via retrieve, not memorized)
- Historical project details (in vault, not in memory)
- Recipe specifics (Paprika handles this)

### Coverage Test Queries

Run each query against the current memory state. Does the agent have enough context to respond, or would it need a vault Read?

| Category | Test Query | Required Context | Expected Score |
|----------|-----------|-----------------|----------------|
| Email triage | "Reply to [collaborator] about the project timeline" | Collaborator's role, email, project relationship | Served |
| Meeting prep | "Prep for the meeting with [person A] and [person B]" | People's roles, project context | Served |
| Project context | "What's the status of [active project]?" | Key people, timeline, org structure | Served |
| Tool use | "Add a task to Todoist for this week" | CLI syntax, project names, priority mapping | Served |
| Vault navigation | "Where do [topic] notes go?" | PARA structure, folder paths | Served |
| Research lookup | "What paper was that about [specific topic]?" | NOT required in memory — vault lookup is fine | Degraded (OK) |
| Active project session | "Resume the [project] work" | Auth details, current phase, next priorities | Served |
| Author lookup | "Who is [author name]?" | NOT required — vault person note covers this | Degraded (OK) |

### Scoring

| Score | Meaning | Action |
|-------|---------|--------|
| **Served** | Memory has enough context — no vault Read needed | Correctly provisioned |
| **Degraded** | Memory has a pointer but needs a Read for specifics | Acceptable for low-frequency queries |
| **Missing** | Memory has no context at all — agent would flounder | Under-provisioned — add to memory |

### Threshold

- All high-frequency queries (email, meeting, project, tool) should score **Served**
- Low-frequency queries (research specifics, author details) can score **Degraded**
- No query should score **Missing**

### When to Run

- After any drain cycle or memory compression
- After deleting or slimming memory files
- At session start if the previous session did memory maintenance

### Post-Test Action

If a high-frequency query scores Degraded or Missing:
1. Identify what context is needed
2. Add an operational summary to the relevant topic memory file (not a full copy — just enough for the access pattern)
3. The vault note stays as the authoritative source; memory gets the quick-ref layer

---

## When NOT to Use Memory-Audit

- **Vault structural health** -> use `/audit` (checks vault notes, not memory files)
- **Note quality review** -> use `/review-note` (per-note content quality)
- **Ontology governance** -> use `/vault-curator` (type vocabulary evolution)
- **Creating a vault note** -> use `/encode` (memory-audit proposes, encode executes)

---

## Reference Files

| File | Role |
|------|------|
| `.claude/rules/typed-relationships.md` | Type taxonomy for classification |
| `.claude/rules/vault-navigation.md` | Navigation patterns (to check POINTER redundancy) |
| `.claude/agent-memory/encode-router/MEMORY.md` | Router memory (to check FEEDBACK graduation) |
| `03 - Resources/Obsidian Reference/Vault Vocabulary.md` | Canonical vocabulary |
