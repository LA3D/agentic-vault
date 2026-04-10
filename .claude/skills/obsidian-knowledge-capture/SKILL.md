---
name: obsidian-knowledge-capture
description: "Use when capturing insights, decisions, or concepts from conversation into vault. Triggers on 'save this', 'remember this', 'create a note about this', 'capture this insight', or when conversation produces knowledge worth preserving. This skill decides WHAT to capture; the /encode skill handles HOW to create the note."
---

# Knowledge Capture

Identify knowledge worth preserving from the current conversation and delegate note creation to the Encode meta-skill. This skill is a domain-specific decision-maker — it figures out what's worth capturing and what type it is. Encode handles routing, templating, wiring, and verification.

**Usage**: `/obsidian-knowledge-capture` or natural triggers ("save this", "remember this", "create a note about this")

---

## Step 1: Identify What's Worth Capturing

Analyze the conversation for knowledge that should persist beyond this session:

| Content Pattern | Suggested Type |
|----------------|---------------|
| Idea, theory, framework | `theory-note` |
| Definition, concept explanation | `concept-note` |
| Procedure, technique, how-to | `method-note` |
| Choice made with rationale | `decision` |
| Experimental result, data point | `finding` |
| Tool, blog post, external link | `external-resource` |
| Quick thought, monitored item | `fleeting-note` |

**Worth capturing if**:
- Connects to an active research area or project
- Represents a reusable insight (not session-specific)
- Would be useful to recall in a future session
- Contains a citable claim, decision rationale, or methodology

**Not worth a vault note** (use Claude memory instead):
- Session-specific context that won't matter next week
- User preferences or interaction patterns (→ `.claude/memory/`)
- Task progress or status updates (→ daily note or tasks)

---

## Step 2: Confirm with User

Present what you plan to capture:

> "I'd suggest saving this as a **concept-note** about [topic]. It connects to [existing vault note]. Want me to create it?"

For obvious cases (user explicitly said "save this"), skip confirmation and proceed.

---

## Step 3: Call Encode

Invoke the `/encode` skill with:

- `content_description`: What the note is about (from conversation context)
- `suggested_type`: From Step 1's type mapping
- `suggested_title`: Your best title suggestion
- `source_material`: Any URLs, citekeys, or inline content from the conversation
- `extra_frontmatter`: Any additional fields (e.g., if the insight came from a specific project, suggest `area:`)

Encode handles everything else: routing, template, frontmatter, MOC wiring, verification, commit, KG rebuild.

---

## Red Flags — STOP

- Capturing something without checking if the vault already covers it (Encode checks, but you should have a sense)
- Creating notes for ephemeral conversation context that won't matter next week
- Forcing connections to the user's specific research when the insight is general (see `.claude/memory/feedback_note_bias.md` or equivalent feedback file for past corrections)
- Capturing vague ideas without enough substance to be useful — if you can't write a meaningful body paragraph, it's not ready for a note

---

## Reference Files

| File | Role |
|------|------|
| `.claude/rules/breadcrumbs-and-typing.md` | Type taxonomy for classification |
| `.claude/rules/linking-guide.md` | Wikilink conventions |
| `.claude/skills/encode/SKILL.md` | Note creation pathway (delegated to) |
