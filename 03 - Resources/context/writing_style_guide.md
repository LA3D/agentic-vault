---
type: reference
up: "[[VAULT-INDEX]]"
---

# Writing and Coding Style Guide

Your preferences for how Claude Code writes — both prose and code. Claude reads this during note creation and review.

> **Customize this file.** These are starting suggestions. Replace them with your actual preferences. The more specific you are, the better Claude matches your voice.

---

## Writing Style

### Default: Brevity and clarity

- Say it once, say it clearly
- Don't repeat the same point in different words
- One idea per paragraph
- Use domain terminology precisely — don't simplify for an imagined audience

### Attribution

- Every claim should trace back to a source (wikilink to literature note, URL, or explicit reasoning)
- "This is true because..." not "This is widely recognized as..."

### Voice

- Active voice preferred
- Direct statements over hedged ones
- Conversational but precise — like explaining to a knowledgeable colleague

---

## Coding Style

> Customize this section based on your languages and preferences.

### General principles

- Brevity facilitates reasoning — shorter code is easier to think about
- One semantic concept per screen
- Comments explain *why*, not *what*
- No auto-formatters unless you explicitly configure them

### Naming

- Use domain-appropriate abbreviations for common things
- Be descriptive for things that appear rarely
- Match the conventions of the language and project

---

## How These Guides Are Used

1. **`/encode`** reads the AI-ese guide when creating notes — avoids flagged patterns during generation
2. **`/review-note`** Agent 4 (Consolidator) checks notes against both files — flags style violations
3. **`/obsidian-research-synthesis`** references the AI-ese guide during synthesis writing
4. **`owner-context.md`** has a summary of your style preferences — this file has the details

Think of `owner-context.md` as the summary and these files as the detailed reference.
