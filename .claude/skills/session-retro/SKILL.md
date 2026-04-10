---
name: session-retro
description: "Use when user says 'retro', 'session review', 'what did we do', 'wrap up', or at end of extended work session"
---

# Session Retrospective

Structured end-of-session reflection. Inventories what happened, captures lessons, and creates a handoff for the next session.

**Usage**: `/session-retro` or natural triggers ("retro", "what did we do", "wrap up", "session review")

---

## Workflow

### 1. Inventory Changes

Run git diff to see what changed this session:

```bash
git diff --name-status HEAD~5  # adjust range based on session length
git status
```

Categorize changes:
- **Created**: New notes, new files
- **Modified**: Updated notes, MOC additions, index updates
- **Other**: Config changes, skill edits, script modifications

### 1.5. Session Health Check

If notes were created or modified this session (identified in Step 1), run `/audit session` to check structural health of the changes. Include the session health results in the retrospective under a "Structural Health" subsection. If any Errors are found, flag them in "What Was Difficult."

### 1.6. Memory Hygiene Check

If memory files were modified this session (check `git diff` against `.claude/projects/*/memory/`), run `/memory-audit session` to classify the changes. Include results in the retrospective under a "Memory Hygiene" subsection. If any KNOWLEDGE classifications are found, flag them in "Open Threads" as drain candidates for next session.

### 2. Generate Structured Reflection

Build the retrospective:

```markdown
## Session Retrospective — YYYY-MM-DD

### What Was Accomplished
- [File/note created or modified] — [one-line description of what and why]
- [Another file] — [description]

### What Worked Well
- [Specific thing that went smoothly — e.g., "vault-kg found the connection between X and Y quickly"]
- [Process that helped — e.g., "design-before-synthesis gate caught a gap in sources"]

### What Was Difficult
- [Gate that blocked progress and why — e.g., "couldn't find 3 sources for synthesis on X"]
- [Rationalization temptation encountered — e.g., "wanted to skip Architect mode"]
- [Technical friction — e.g., "import file had encoding issues"]

### Open Threads
- [Topic not finished — what state it's in]
- [Notes with `curator_status: pending`]
- [Questions raised but not answered]
- [Tasks created but not completed]

### Next Session Setup
- **Start with**: [Specific action — e.g., "Read the 3 papers found in Explore mode"]
- **Mode**: [If research-session, which mode to start in]
- **Priority**: [What matters most next]
```

### 2.5. Multi-Session Pattern Detection

Scan recent daily notes for recurring themes that should become vault notes:

1. Read the last 3-5 daily notes: `ls -t Daily/*.md | head -5`
2. Look for patterns:
   - Repeated wikilinks across sessions (same concept appearing in 3+ retros)
   - Recurring "Open Threads" that never resolve (may need a dedicated note)
   - Same topic discussed in multiple session retrospectives
3. If a concept or idea appears in 3+ sessions without a dedicated vault note:
   - Flag it in this retro's "Open Threads": "Recurring pattern: [topic] appeared in [N] sessions. Consider promoting to a concept note via `/encode`."
4. This is the proactive drain — catching knowledge forming in conversation before it settles into memory files.

### 3. Append to Daily Note

Add the retrospective to today's daily note under a "Session Retrospective" section.

If no daily note exists, create one with the retrospective as its initial content.

### 4. List Uncommitted Changes

```bash
git status
```

If uncommitted changes exist:
- List them for the user
- Suggest a commit message
- Ask if user wants to commit now

---

## Lightweight Mode

For short sessions (< 30 minutes or < 3 files changed), produce a condensed retro:

```markdown
## Quick Retro — YYYY-MM-DD
- [What was done in 1-2 bullets]
- Next: [What to pick up next]
```

---

## Red Flags — STOP

- Fabricating accomplishments not reflected in git diff
- Skipping the "Open Threads" section (this is the handoff — it's the most important part)
- Writing a retro longer than the work it describes

---

## Related Skills

- **research-session**: Ship mode produces a session summary; retro adds reflection on top
- **project-planning**: Open threads may suggest project task updates
