# Discipline Gates

Cross-skill enforcement patterns. These rationalizations and gate definitions apply to ALL note-creation and review skills.

---

## Universal Rationalizations (Always Wrong)

| Rationalization | Why It's Wrong | Affected Skills |
|----------------|----------------|-----------------|
| "I'll add links/frontmatter later" | Later never comes. Do it now while context is fresh. | All note-creation skills |
| "Just a quick note" | Quick notes become permanent orphans. Use `05 - Watching/` with `type: fleeting-note` and `status: watching` for items being monitored. Inbox is a processing queue, not a home. | obsidian-knowledge-capture, encode |
| "Review can wait" | Post-hoc review costs more than inline verification. Check now. | review-note, obsidian-research-synthesis |
| "I have enough sources" | Minimum 3 for synthesis. Query vault-kg. Single-source "synthesis" is paraphrasing. | obsidian-research-synthesis, research-session |
| "Good enough to commit" | Read it back first. Verification-before-completion is non-negotiable. | All skills with commit steps |
| "I'll update the MOC/index separately" | Unindexed notes are invisible. Update in the same session. | All note-creation skills |
| "I already know this note is good" | You wrote it. Same blind spots. Run `/review-note --draft` — it's cheap. | encode, batch ingest skills |
| "These notes all agree" | You read them in the same session with the same mental model. Check `concept:` neighbors for silent contradictions. | retrieve, obsidian-research-synthesis |

---

## Gate Types

### Design Gate
**What**: Plan before executing. Present plan to user for approval.
**Where used**: research-synthesis (synthesis plan), research-session (mode transitions), project-planning (PLAN.md)
**Pattern**: Gather → Assess → Propose plan → Get approval → Execute

### Verification Gate
**What**: Read back created work and check against concrete criteria before committing.
**Where used**: All note-creation skills, batch ingest workflows
**Pattern**: Create → Read back → Check criteria list → Fix failures → Commit

### Sequential Gate
**What**: Step N must pass before Step N+1 can begin.
**Where used**: review-note (structural must pass before content review), research-session (3+ sources before Synthesize mode)
**Pattern**: Run Step N → Check pass criteria → If fail: fix and re-run → If pass: proceed to N+1

---

## Skill Dependency Chain [MUST FIRE]

Skills that depend on other skills. When a upstream skill runs, the downstream skill MUST run — not "should," not "consider," MUST.

| When this runs... | ...this MUST also run | Why |
|---|---|---|
| `/encode` (note creation) | `/review-note --draft` on the created note | Catch structural errors and silent contradictions before commit |
| Batch ingest (e.g., Readwise, Zotero import, manual capture) | `/review-note --draft` on each created note | Ingest is the highest-risk moment for contradiction introduction |
| `/obsidian-research-synthesis` | `/review-note --final` on the synthesis note | Synthesis compounds errors from sources — needs adversarial review |
| `/retrieve` (loading context) | Contradiction scan across loaded notes | Don't build on inconsistent foundations — check before presenting |
| `/session-retro` | `/audit session` on notes touched this session | End-of-session structural health check |

### Contradiction Detection Triggers

Contradiction detection is NOT a standalone operation. It fires as part of existing skills:

1. **During `/review-note`** (Agent 2 — Content Accuracy): Query notes sharing `concept:` edges with the reviewed note. Read their key claims. Flag unacknowledged contradictions — tensions are fine if explicit (`criticizes:` edge or prose acknowledgment), silent disagreement is a data integrity problem.

2. **During `/retrieve`** (context loading): When loading 3+ notes into working memory that share `concept:` or `up:` targets, scan for claim conflicts before presenting the context. Report tensions to the user: "Note A says X, Note B says Y — which framing should we work from?"

3. **During `/audit`** (vault-wide lint): Find concept nodes with 3+ notes pointing at them. For each cluster, check for accumulated drift — claims that were consistent when written but diverged as the vault evolved.

---

## Applying Gates

When working on ANY note-creation or knowledge-capture task:

1. **Before creating**: Did I search for existing coverage? (Design gate)
2. **During creating**: Am I using canonical types, proper edge fields, correct location? (Inline discipline)
3. **After creating**: Did I read it back and verify? (Verification gate)
4. **After verifying**: Did I run `/review-note --draft`? (Review gate)
5. **Before committing**: Are MOCs/indexes updated? Are all links valid? (Commit gate)

If you catch yourself thinking any phrase from the rationalization table above, that's the signal to slow down and follow the gate, not skip it.
