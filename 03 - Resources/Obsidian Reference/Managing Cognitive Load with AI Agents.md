---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - cognitive-load
  - methodology
  - sustainability
---

# Managing Cognitive Load with AI Agents

> The vault's skill patterns aren't just organizational — they're cognitive load management. AI agents can intensify work faster than you realize. This note explains why the vault is structured the way it is.

---

## The Problem: AI Intensifies Work

Research from Berkeley Haas (Ranganathan & Ye, 2026) studying 200 employees found that AI tools don't reduce work — they intensify it. Workers managed several active threads at once, ran multiple agents in parallel, and revived long-deferred tasks because AI could "handle them." The result was cognitive overload disguised as productivity.

As Simon Willison observed: "I can get *so much done*, but after just an hour or two my mental energy for the day feels almost entirely depleted."

The trap: AI makes each individual task faster, so you take on more tasks simultaneously. The *throughput* increases but the *cognitive overhead* of directing, reviewing, and integrating all that output accumulates. You feel productive while burning out.

Source: [AI Doesn't Reduce Work—It Intensifies It](https://simonwillison.net/2026/Feb/9/ai-intensifies-work/) (Willison, linking to HBR)

---

## How This Vault Addresses It

The vault's skill patterns are designed to create sustainable working rhythms with AI agents. They impose structure that your brain won't impose on itself when the agent is offering to do "just one more thing."

### Research Sessions Have Modes and Gates

The `/research-session` skill has 5 modes (Explore → Architect → Synthesize → Critique → Ship) with **hard gates** between them. You can't synthesize without 3+ sources. You can't critique without something to critique. You can't skip Ship mode.

**Why**: Without modes, a research session becomes an endless Explore spiral — the agent keeps finding interesting things, you keep saying "ooh, follow that." The gates force you to stop gathering and start making sense of what you have. Time-box suggestions (20 min per mode) give you permission to stop.

### Session Retros Force Reflection

The `/session-retro` skill runs at the end of a work session. It asks: what did we accomplish, what was difficult, what should we do next time?

**Why**: Without retros, sessions blend together. You lose track of what you decided and why. The daily note becomes the handoff between "today you" and "tomorrow you" — a form of cognitive offloading that lets you actually stop working.

### Discipline Gates Prevent Shortcuts

The discipline gates in `.claude/rules/discipline-gates.md` list rationalizations that are "always wrong" — things like "I'll add links later" and "good enough to commit." Each has a gate that prevents the shortcut.

**Why**: AI speed creates pressure to skip verification. The agent creates a note in 10 seconds, so reading it back feels wasteful. But unverified notes compound into structural debt — broken links, mistyped relationships, silent contradictions. The gates slow you down at the moments where speed causes the most damage.

### Verification Before Completion

Every note created by `/encode` is read back and checked before commit. Every synthesis note gets a `/review-note --final`. The system never assumes its own output is correct.

**Why**: The human tendency is to trust fluent output. If it reads well, it must be right. But LLM output can be confidently wrong — especially for factual claims, attribution, and relationship typing. The verification gate catches errors when they're cheap to fix.

### The Pullein Time Budget

The task management rule recommends planning no more than 50% of your time. Pullein's insight: flexibility matters more than a full schedule.

**Why**: AI makes it possible to fill every hour with productive work. That's exactly when you need the discipline to leave slack. Unexpected tasks, creative thinking, and recovery all need unscheduled time. A fully utilized schedule is a fragile schedule.

---

## Adapting the Patterns to Your Style

These patterns encode one person's cognitive strategies. Yours may differ. The vault is designed to be adapted — the structure is the scaffold, your preferences fill it in.

### Where Your Cognitive Preferences Live

The vault stores your working style in several places, each serving a different purpose:

| File | What it controls | How to change |
|------|-----------------|---------------|
| `.claude/rules/owner-context.md` | Interaction style — how Claude talks to you, what to explain vs. assume, your expertise level | Edit directly or re-run `/onboarding` |
| `03 - Resources/context/ai_ese.md` | Writing patterns to avoid — what makes text feel artificial *to you* | Add patterns that bother you, remove ones you don't care about |
| `03 - Resources/context/fastai_style_guide.md` | Coding style — brevity, naming, layout (optional, customizable) | Adopt what resonates, replace for your domain |
| `.claude/rules/discipline-gates.md` | Verification checkpoints — which shortcuts to block | Adjust gate strictness to match your risk tolerance |

Claude reads these every session. They're the "personality layer" of the vault — the same structural skills (encode, retrieve, review) behave differently based on these preferences.

### Specific Dimensions to Tune

- **Session length**: If you find yourself depleted after 90 minutes, set that as your default session length. Run `/session-retro` before you're exhausted, not after.
- **Mode time-boxes**: The 20-minute suggestion per research mode is a starting point. Some people think in longer arcs; adjust to what sustains your focus.
- **Verification depth**: `--draft` mode in `/review-note` is lighter than `--final`. Use draft during exploration, final before publishing or sharing.
- **Parallel work**: The vault supports multiple projects, but the research on AI intensification suggests limiting active threads. Consider focusing on one project per session rather than context-switching between three.
- **Communication style**: Some people want Claude to push back and debate. Others want it concise and deferential. Set this in `owner-context.md` and Claude adjusts.
- **Domain expertise**: If you're an expert in a field, tell Claude in `owner-context.md` so it doesn't over-explain things you already know. If you're learning a new domain, note that too — Claude adjusts its explanation depth.

### The Style Guides as Cognitive Load Reduction

The style guides (`ai_ese.md` and `writing_style_guide.md`) aren't just aesthetic preferences — they're cognitive load reducers. Every AI-ese phrase Claude avoids is one you don't have to mentally edit while reading. Every domain term it uses correctly is one you don't have to correct. Over hundreds of notes, this compounds.

Start with the defaults, then refine as you notice patterns that bother you. The `/review-note` skill checks against these files, so they actively prevent drift rather than just documenting ideals.

---

## For Reference

- `.claude/rules/discipline-gates.md` — The specific gates and rationalizations
- `.claude/skills/research-session/SKILL.md` — The 5-mode research session structure
- `.claude/skills/session-retro/SKILL.md` — End-of-session reflection pattern
- `03 - Resources/context/ai_ese.md` — AI writing patterns to avoid (customize)
- `03 - Resources/context/fastai_style_guide.md` — Coding style guide (optional, customizable)
- [[Vault Architecture]] — How the skill layers implement a cognitive architecture
