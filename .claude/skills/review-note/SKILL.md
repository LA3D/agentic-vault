---
name: review-note
description: "Review a single vault note for structural compliance, content accuracy, vault integration, and style quality. Use when the user asks to review, check, or QA a specific note, or after creating batch notes. Accepts a note path as argument. Spawns parallel specialist agents that check against the vault's type taxonomy, edge field schema, and style guide, then consolidates findings into a severity-ranked report. Also triggers when user says 'review this', 'check this note', 'is this note good', or 'QA the notes we just created'. For vault-wide structural health checks, use /audit instead."
---

# Review Note

Quality review for vault notes using parallel specialist agents with contrastive grounding. Each agent checks one dimension against the vault's concrete standards, then a consolidator synthesizes findings.

**Usage**: `/review-note path/to/note.md` or `/review-note path/to/folder/` (batch)

Optional flags (append after path):
- `--draft` — gentle review, flag only clear errors (discovery/drafting phase)
- `--final` — adversarial review, stress-test every claim (pre-commit quality gate)
- Default is `--final` if no flag given.

---

## Why Contrastive Grounding Matters

The self-critique paradox: when an LLM reviews its own output without external reference, it either rubber-stamps (missing real errors) or hallucinates issues (turning 98% accuracy into 57%). The fix is contrastive grounding: give the critic concrete standards to check against.

This vault has strong reference material:
- **Type taxonomy**: `03 - Resources/Obsidian Reference/Vault Vocabulary.md`
- **Edge field schema**: `.claude/rules/typed-relationships.md`
- **Style guide**: `03 - Resources/context/ai_ese.md`
- **Existing notes**: The vault itself shows correct patterns

Every review agent gets the relevant reference material. They check the note against these standards, not against self-generated expectations.

---

## Gate Structure [NON-NEGOTIABLE]

Review proceeds through two sequential gates. Gate 2 CANNOT run until Gate 1 passes.

### Gate 1: Structural Compliance (must pass first)

Run Agent 1 (Structural Compliance) alone. If it returns ANY **Error**-severity findings:

1. **Stop**. Do not run Agents 2-3.
2. Fix all structural errors (missing `type:`, broken edge fields, deprecated fields).
3. Re-run Agent 1 to confirm zero Errors.
4. Only then proceed to Gate 2.

**Why**: Content and integration reviews are meaningless if the note's structure is broken. Fixing structure first prevents cascading false positives in later agents.

### Gate 2: Quality Review

After Gate 1 passes with zero Errors, run Agents 2 (Content), 3 (Integration), and 4 (Consolidator) in parallel.

### Rationalization Table

| Temptation | Why It's Wrong |
|------------|----------------|
| "The note looks fine to me" | You wrote it. Same blind spots. Check against reference material. |
| "I'll just do a quick general review" | General reviews miss specific issues. Specialist agents catch more with narrow focus. |
| "Style doesn't matter for this note" | AI-ese erodes trust. The project's style guide exists because this matters. Flag it. |
| "I'll check links later" | Broken links are the #1 integration issue. Check now while context is fresh. |
| "It's just a draft, don't need full review" | Use `--draft` flag explicitly. Don't skip the gate — use the right gate level. |

---

## Architecture

Three parallel specialist agents + one consolidator. Each specialist is biased toward over-reporting (better to flag a non-issue than miss a real one). The consolidator is biased toward dismissing false positives.

### Agent 1: Structural Compliance

**Checks against**: Vault Vocabulary type taxonomy + edge field domain/range constraints

- [ ] `type:` present and from canonical taxonomy
- [ ] `type:` matches the note's actual content (not just structurally valid but semantically correct)
- [ ] Required edge fields populated for this type:
  - Literature notes: `up:`, `authors:`, `year:`, `title:`, `concept:` or `source:`
  - External resources: `up:`, `area:`
  - Theory/concept notes: `up:`, `extends:` or `source:`
  - Projects: `area:`, `status:`
- [ ] Edge field domain/range: `concept:` points to concept/theory/method notes, `source:` points to literature, etc.
- [ ] `created:` date present
- [ ] Tags present and relevant (not empty, not generic)
- [ ] No deprecated fields (`noteType:`, `relatedConcepts:`, `relatedLiterature:`, `implementations:`)

**Reference files to read**:
- `03 - Resources/Obsidian Reference/Vault Vocabulary.md`
- `.claude/rules/typed-relationships.md`

### Agent 2: Content Accuracy

**Checks against**: Source material (if available) + existing vault notes on the same topic

- [ ] Summary accurately represents the source (no strawman, no conceptual drift)
- [ ] Claims are attributed (no orphaned assertions)
- [ ] Author names and dates correct
- [ ] URLs are plausible (not hallucinated)
- [ ] Key contributions/findings faithfully captured
- [ ] No conflation of different sources or concepts
- [ ] No unacknowledged contradictions with vault neighbors (notes sharing `concept:`, `up:`, or `supports:`/`criticizes:` targets). If tension exists, it should be explicit — via `criticizes:` edge or prose acknowledgment, not silent disagreement.

**For this agent**: Read the note, then read its `source:` or `readwise:` linked file if available. If the note references a paper or URL, verify key claims match. Query for notes sharing `concept:` edges with this note — read their key claims and check for silent contradictions. Two notes disagreeing is scholarship; two notes silently contradicting each other is a data integrity problem.

### Agent 3: Integration Quality

**Checks against**: MOC structure, existing backlinks, vault indexes

- [ ] `up:` points to an existing MOC or index
- [ ] Listed in the relevant MOC or sub-index (LITERATURE-INDEX, EXTERNAL-INDEX)
- [ ] Wikilinks in body text resolve to existing notes (check for broken links)
- [ ] Bidirectional linking: notes that should link TO this note (check if the MOC actually references it)
- [ ] No duplicate coverage (search vault for existing notes on same topic/paper)
- [ ] For projects: `area:` connects to an Area of Focus

**For this agent**: Use Glob and Grep to verify links resolve. Read the MOC referenced in `up:` to check if this note is listed.

### Agent 4: Consolidator (Skeptic)

**Checks against**: All findings from agents 1-3 + style guide

After the three specialists report:

1. **Dismiss false positives**: If a finding is debatable or the note is arguably correct, dismiss it.
2. **Style check** (lightweight): Scan for AI-ese patterns from `03 - Resources/context/ai_ese.md`. Only flag egregious cases.
3. **Severity ranking**: Assign each confirmed finding a severity:
   - **Error** — wrong type, broken links, factual inaccuracy, missing required fields
   - **Warning** — suboptimal but not wrong: missing optional fields, weak integration, style issues
   - **Suggestion** — improvement opportunities: better connections, richer linking, conceptual depth
4. **Score** (optional, for `--final` mode): 0-100 based on rubric below.

---

## Scoring Rubric (--final mode only)

| Dimension | Weight | 100 = | 0 = |
|-----------|--------|-------|-----|
| Structural compliance | 25% | All fields correct, canonical type, proper edges | Missing type, broken schema |
| Content accuracy | 30% | Faithful to source, no drift, claims attributed | Hallucinated claims, strawman |
| Integration | 25% | Listed in MOC, bidirectional links, no orphan | Orphan note, no MOC, broken links |
| Style | 20% | No AI-ese, domain-appropriate, concise | Heavy AI-ese, over-explained |

**Thresholds** (from Sant'Anna):
- 95+ = excellent, ready for sharing
- 90+ = solid, minor polish only
- 80+ = acceptable, some issues to fix
- <80 = needs revision before committing

---

## Running the Review

### Single Note

```
/review-note 03 - Resources/Literature/@chen-2026-cot-controllability.md
```

1. Read the target note
2. Spawn 3 specialist agents in parallel (Agent tool), each reading their reference files and the target note
3. Collect findings
4. Run consolidator (can be inline, doesn't need a subagent)
5. Output the review report

### Batch Review

```
/review-note 03 - Resources/Coding Agents for Research/ --draft
```

For batch review of a folder:
1. List all `.md` files in the folder
2. For each file, run a lightweight single-pass review (no subagents, just inline checks)
3. Output a summary table: note name, type, score estimate, top issue

Batch mode is always `--draft` severity regardless of flag, to keep token cost manageable.

---

## Review Report Format

```markdown
## Review: [Note Title]

**Path**: `path/to/note.md`
**Type**: literature-note | Score: 87/100
**Mode**: --final

### Errors (must fix)
1. **[Integration]** Note not listed in LITERATURE-INDEX.md under any topic section
2. **[Content]** Author listed as "Korbak et al." but first author is Y.-H. Chen (Korbak is blog post author)

### Warnings (should fix)
1. **[Structural]** Missing `literatureType:` field (optional but recommended for literature-note)
2. **[Style]** Line 42: "stands as a key contribution" — AI-ese pattern

### Suggestions (consider)
1. **[Integration]** Could link to [[Trusted AI Principles]] — conceptual overlap on monitorability
2. **[Content]** The "Key Contributions" section could note the open-source eval suite (CoT-Control) more prominently

### Summary
Solid note with proper frontmatter and good vault connections. Main gap is missing from LITERATURE-INDEX. Style is clean with one minor AI-ese flag.
```

---

## Severity Calibration by Mode

### --draft (gentle)
- Only report Errors
- Skip style checking entirely
- Skip integration checking (note may not be indexed yet)
- No score

### --final (adversarial)
- Report all: Errors, Warnings, Suggestions
- Full style check against AI-ese guide
- Full integration check (MOC listing, bidirectional links)
- Score with rubric

---

## Common Mistakes

| Excuse | Reality Check |
|--------|--------------|
| "The note looks fine to me" | You wrote the note. You have the same blind spots. Check against the reference material. |
| "I'll just do a quick general review" | General reviews miss specific issues. The specialist agents exist because narrow focus catches more. |
| "The style issues don't matter" | AI-ese erodes trust. The project's style guide exists because this matters. Flag it. |
| "I'll check links later" | Broken links are the #1 integration issue. Check now while context is fresh. |

---

## Red Flags — STOP

- Running a review without reading the vault's reference files (Vault Vocabulary, typed relationship rules)
- Rubber-stamping a note as "looks good" without checking specific dimensions
- Reporting a finding you're not confident about without marking it as low-confidence
- Reviewing more than 10 notes in batch mode without stopping to show the user interim results

---

## Reference Files

These files provide the contrastive grounding that makes review effective:

| File | What It Provides | Agent |
|------|-----------------|-------|
| `03 - Resources/Obsidian Reference/Vault Vocabulary.md` | Canonical types, edge domain/range | Agent 1 |
| `.claude/rules/typed-relationships.md` | Required fields per type, deprecation list | Agent 1 |
| `03 - Resources/context/ai_ese.md` | AI writing patterns to avoid | Agent 4 |
| `03 - Resources/context/fastai_style_guide.md` | Brevity, clarity, domain awareness | Agent 4 |
| Source material (varies) | Ground truth for content accuracy | Agent 2 |
| Relevant MOC (varies) | Integration verification | Agent 3 |
