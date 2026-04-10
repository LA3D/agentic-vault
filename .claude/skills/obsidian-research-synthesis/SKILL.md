---
name: obsidian-research-synthesis
description: "Use when synthesizing research into a NEW note — combining 3+ vault sources into a structured argument, theory, or analysis. Triggers on 'synthesize X', 'build an argument about X', 'write up what we know about X', 'create a synthesis note'. This skill CREATES output (a new synthesis note); for finding/retrieving existing notes use /retrieve instead."
---

# Research Synthesis

Synthesize findings from multiple vault notes into a structured theory, concept, or argument note. Design-before-synthesis: plan the synthesis, get approval, then execute.

**Usage**: `/obsidian-research-synthesis [topic]`

---

## Design Gate [NON-NEGOTIABLE]

Before writing ANY synthesis content, complete ALL of these steps:

### 1. Query Vault for Source Material

```bash
obsidian search vault="obsidian" query="[topic]" limit=15
```

Also check:
- Relevant MOC for existing coverage (`obsidian links file="[MOC Name]"`)
- LITERATURE-INDEX for related papers
- EXTERNAL-INDEX for related external resources
- Use `vault-kg` skill if graph queries would help find connections

### 2. Read and Assess Sources

Read each relevant note. Build a source list with:
- Note path
- Key claim or finding from that note
- How it connects to the synthesis topic

**Minimum 3 source notes required.** If fewer than 3 exist, tell the user and suggest what notes to create first. Do not synthesize from insufficient evidence.

### 3. Present Synthesis Plan to User

Before writing, present:

```markdown
## Proposed Synthesis: [Title]

**Thesis**: [One sentence — the argument this note will make]
**Type**: [theory-note | concept-note | method-note | finding]
**Location**: [Full vault path]
**Parent MOC**: [Which MOC this will be listed under]

### Sources (minimum 3):
1. [[Source Note 1]] — [what it contributes]
2. [[Source Note 2]] — [what it contributes]
3. [[Source Note 3]] — [what it contributes]

### Proposed Structure:
- [Section 1 heading]
- [Section 2 heading]
- [Section 3 heading]

### Gaps: [What's missing, what claims need more support]
```

**Wait for user approval before proceeding.** If the user suggests changes, revise the plan.

---

## Synthesis Execution

After approval:

### 4. Create Note with Proper Frontmatter

```yaml
---
created: YYYY-MM-DD
type: [theory-note | concept-note | method-note | finding]
up: "[[Relevant MOC]]"
area: "[[Research & Scholarship]]"
extends: "[[Note This Builds On]]"  # if applicable
source:
  - "[[Literature source]]"
concept:
  - "[[Related Concept]]"
supports:  # or criticizes:
  - "[[Claim]]"
tags:
  - topic-tags
---
```

### 5. Write Synthesis Content

- Use claim-form title when possible (e.g., "Structure Helps Agents Navigate Better Than Embeddings Alone")
- Attribute every claim to a source note via wikilink
- Use edge fields for typed relationships
- Follow vault style (no AI-ese, see `03 - Resources/context/ai_ese.md`)
- Keep to 200-400 words for the core argument; link out for depth

### 6. Update MOC

Add the new note to the relevant MOC section. If no appropriate section exists, create one.

---

## Post-Write Verification Gate [NON-NEGOTIABLE]

Before committing, read the note back and verify:

- [ ] All frontmatter fields populated (no placeholders)
- [ ] `type:` is a canonical value
- [ ] `up:` target MOC exists and lists this note
- [ ] Every claim in the body has a wikilink attribution
- [ ] All wikilinks resolve to existing notes (Glob check)
- [ ] `source:` or `concept:` edges point to real notes
- [ ] No AI-ese patterns (check against `ai_ese.md`)
- [ ] Note appears in the correct MOC section

If ANY check fails → fix before committing.

---

## Commit

```bash
git add [note file] [MOC file]
git commit -m "$(cat <<'EOF'
[Agent: Claude] Add [type] synthesis: [title]

- Synthesized from [N] source notes
- Added to [MOC name]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Rationalization Table

| Temptation | Why It's Wrong |
|------------|----------------|
| "I have enough with 1-2 sources" | Minimum 3. Synthesis from fewer sources is just paraphrasing. Check vault-kg for more. |
| "I'll add citations later" | Unattributed claims are orphaned assertions. Cite now or don't claim. |
| "Doesn't need the MOC update" | Unindexed notes are invisible. Update the MOC in the same session. |
| "The synthesis is obvious, skip the plan" | The plan is for alignment, not complexity. Present it. User may see gaps you don't. |
| "Good enough to commit" | Read it back first. Verification-before-completion is non-negotiable. |

---

## Red Flags — STOP

- Writing synthesis without reading source notes first
- Synthesizing from memory or training data instead of vault content
- Creating a note that duplicates existing vault coverage (search first)
- Skipping the design gate when user explicitly asked for a synthesis

---

## Related Skills

- **vault-kg**: Graph queries to find source connections
- **review-note**: Post-creation quality review (`/review-note --final`)
- **encode**: For creating individual typed notes (not synthesis)
- **research-session**: Synthesis is one mode within a structured research session
