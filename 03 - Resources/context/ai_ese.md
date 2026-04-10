---
type: reference
up: "[[VAULT-INDEX]]"
---

# AI Writing Patterns to Avoid

This file trains Claude Code to avoid common LLM writing patterns that make text feel artificial. Claude reads this during note review (`/review-note`) and note creation (`/encode`, `/obsidian-research-synthesis`).

> **Customize this file.** Add patterns that bother you. Remove ones you don't care about. The goal is that notes in your vault read like *you* wrote them, not like an AI generated them.

---

## Why This Matters

AI-generated text has recognizable patterns — inflated importance, promotional tone, hedge phrases, and structural tics. When your vault accumulates these patterns, two things happen:

1. **Trust erodes** — you stop reading your own notes carefully because they feel generic
2. **Review burden increases** — you spend cognitive effort editing out AI-ese instead of thinking about content

A style guide reduces this burden by preventing the patterns at generation time.

---

## Language and Tone

### Undue emphasis on importance

Words to watch: *stands as a testament*, *plays a vital/significant role*, *underscores its importance*, *continues to captivate*, *leaves a lasting impact*, *watershed moment*, *key turning point*, *deeply rooted*, *profound*, *solidifies*

LLMs inflate the importance of whatever they're writing about. A concept note about a method doesn't need to "stand as a testament to the power of structured reasoning."

### Promotional language

Words to watch: *rich cultural heritage*, *breathtaking*, *stunning*, *must-see*, *enduring legacy*, *rich tapestry*, *vibrant*, *fascinating glimpse*

### Hedge phrases that add nothing

Words to watch: *it's important to note*, *it is worth noting*, *it's worth mentioning*, *no discussion would be complete without*, *it should be noted that*

If something is important enough to say, just say it. The hedge phrase wastes tokens and signals uncertainty you probably don't intend.

### Filler transitions

Words to watch: *delving into*, *navigating the*, *in the realm of*, *the landscape of*, *at its core*, *fundamentally*

### Excessive summarization

Don't end sections with "In summary, ..." or "In conclusion, ..." unless the section is genuinely long enough to need it. Don't begin responses with "Great question!" or "That's an interesting point."

---

## Formatting

### Minimal bold emphasis

Don't bold every other phrase for emphasis. Bold sparingly — if everything is emphasized, nothing is.

### No emoji unless asked

Don't add emoji to notes, commit messages, or responses unless the user requests it.

### Appropriate heading depth

Don't use ### for every sub-point. Let prose do the work. Reserve headings for genuine structural divisions.

---

## Adapting This Guide

This file is a starting point. Good additions:

- **Domain jargon you hate**: terms from your field that LLMs misuse
- **Phrases you never use**: if you'd never write "leverage" or "utilize," add them here
- **Structural preferences**: do you prefer bullet points or prose? Short paragraphs or long?

The `/review-note` skill's Agent 4 (Consolidator) checks notes against this file. The more specific your guide, the more useful the review.
