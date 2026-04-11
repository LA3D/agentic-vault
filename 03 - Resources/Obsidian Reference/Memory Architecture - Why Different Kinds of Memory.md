---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - cognitive-architecture
  - memory-systems
  - coala
---

# Memory Architecture — Why Different Kinds of Memory

> This vault has several distinct places where "memory" lives. This isn't accidental — it follows a cognitive architecture framework from research on language agents. Understanding why there are different kinds of memory helps you work with the system rather than fighting it.

---

## The Framework: CoALA

This vault's memory architecture is grounded in **CoALA** (Cognitive Architectures for Language Agents), a framework by Sumers et al. (2023, Princeton) that maps 50 years of cognitive architecture research onto LLM agents. CoALA identifies four types of memory that intelligent systems need, each serving a different purpose.

The key insight: **different kinds of knowledge have different access patterns, different lifespans, and different costs.** Cramming everything into one memory system forces tradeoffs that separate systems avoid.

Source: Sumers, T.R., Yao, S., Narasimhan, K., & Griffiths, T.L. (2023). "Cognitive Architectures for Language Agents." TMLR 2024. arXiv:2309.02427

---

## Four Memory Types and How This Vault Implements Them

### 1. Working Memory (the context window)

**What it is**: Everything Claude can see right now — the active conversation, loaded files, current goals. Fast but expensive and limited. Every token of working memory competes with the task for attention.

**Vault implementation**:
- `CLAUDE.md` — loaded at session start, provides orientation (~150 lines)
- `.claude/rules/` — 7 rule files loaded at session start, provide behavioral guidance (~700 lines)
- Together these consume ~850 lines of context window before the conversation starts

**Why it's separate**: Working memory is the scarcest resource. Everything loaded here displaces conversation and reasoning tokens. That's why CLAUDE.md has a 200-line recommended limit, why rules are modular (so they could be path-scoped in the future), and why skills load on demand rather than at startup.

**The design tension**: More context makes Claude more capable (it knows more). But more context also makes Claude less effective (less room for reasoning). Progressive disclosure is the resolution — load the routing table (VAULT-INDEX), not the entire vault.

### 2. Procedural Memory (how to do things)

**What it is**: Knowledge about *how to act* — procedures, workflows, patterns. Exists in two forms: implicit (in the LLM's weights, from pre-training) and explicit (inspectable documents you can read and edit).

**Vault implementation**:
- **Explicit**: `.claude/skills/` — 14+ skill files that describe procedures step by step. Each skill is a detailed protocol: when to trigger, what steps to follow, what gates to check, how to verify.
- **Implicit**: Claude's pre-trained knowledge of how to write markdown, use git, reason about concepts, etc.
- **Style guides**: `03 - Resources/context/ai_ese.md` and `fastai_style_guide.md` — procedural knowledge about *how to write*

**Why it's separate**: Procedural memory loads on demand, not at startup. A skill like `/encode` (400+ lines) only enters the context window when invoked. If all skills loaded at startup, they'd consume ~6000 tokens before you said anything. The on-demand loading pattern keeps working memory lean.

**The inspectability advantage**: Unlike the LLM's implicit knowledge (which you can't read or edit), the vault's explicit procedural memory is plain text. You can read a skill, understand why it does what it does, edit it to change behavior, and verify it's correct. When Claude makes a procedural mistake, you fix the skill — not retrain the model.

### 3. Episodic Memory (what happened)

**What it is**: Records of past experiences — what was done, what was decided, what worked and what didn't. Episodic memory lets you learn from history without re-experiencing it.

**Vault implementation**:
- **Auto memory** (`~/.claude/projects/<project>/memory/`) — Claude's own learning notes. Claude writes these automatically when it discovers something worth remembering: build commands, debugging insights, your preferences, patterns it noticed. The first 200 lines of `MEMORY.md` load at session start.
- **Daily notes** (`Daily/YYYY-MM-DD.md`) — session journals capturing what was worked on, decisions made, open questions. Written by the `/session-retro` skill.
- **Subagent memory** (`.claude/agent-memory/`) — persistent memory for skill subagents. The encode Router stores routing corrections here so it learns from mistakes.

**Why it's separate**: Episodic memory is personal and temporal — it's *your* history with *this* vault. It accumulates over time and should be prunable. Auto memory is machine-local and not shared via git. Daily notes are commitable but ephemeral. Neither belongs in CLAUDE.md (which is structural, not temporal) or in skills (which are procedural, not experiential).

### 4. Semantic Memory (what you know)

**What it is**: Factual knowledge about the world — concepts, theories, evidence, connections between ideas. The long-term knowledge store that grows as you learn.

**Vault implementation**:
- **Typed vault notes** — concept notes, theory notes, literature notes, implementation notes, etc. in `03 - Resources/`. Each has a `type:` and typed edge fields (`up:`, `concept:`, `source:`, `extends:`, etc.)
- **MOCs** (Maps of Content) — curated navigation hubs for topic areas
- **Knowledge graph** — the SPARQL-queryable RDF graph built from frontmatter edge fields via `scripts/kg/`
- **Sub-indexes** — exhaustive catalogs like LITERATURE-INDEX

**Why it's separate**: Semantic memory is the vault's core value — it's what you're building over time. It's persistent (doesn't expire), structured (typed relationships), queryable (SPARQL), and navigable (progressive disclosure). Unlike working memory (limited, expensive), semantic memory is unlimited — the vault can hold thousands of notes without any context window cost. Claude loads semantic memory *selectively* via progressive disclosure, paying context cost only for the notes it actually reads.

---

## Structural Constraints on Semantic Memory

CoALA tells you *which* memory types a language agent needs. It does not tell you *how to structure them so retrieval stays correct as they grow*. That second question is where the structural constraints of this vault come from, and they are important enough to be their own section.

**The short version**: as semantic memory grows, **flat retrieval** (cosine similarity over a single embedding space) hits a mathematical ceiling on correctness that cannot be engineered away by better models or more training. The ceiling is real, it is provable, and it applies to every memory architecture that retrieves by meaning without external grounding. The only escape is **hierarchical retrieval with bounded branching** — the same pattern this vault uses for MOCs, sub-indexes, and typed edges.

Three specific structural principles follow:

### Principle 1 — Bounded branching (the Fano bound)

Every navigation node (a MOC section, an index subsection, a folder treated as a namespace) has a maximum branching factor beyond which an agent cannot reliably pick the right child from a query. The information-theoretic bound is $n_k \leq 12$ at each level (derived from Fano's inequality applied to routing-as-classification with ~2 bits of mutual information per step). Above this, routing error grows quickly; below it, error stays bounded regardless of total vault size.

**Practical consequence**: if a MOC section has 40 direct entries, split it into subsections. If a folder has 150 files, split into subfolders or introduce a sub-index. The vault's `/audit` skill checks this automatically (Check F — Branching Factor) and flags violations as warnings or errors.

See `[[Bounded Branching - Why This Skill Checks the Fano Bound]]` for the full methodology argument.

### Principle 2 — Typed edges as interface operations

Edge fields (`concept:`, `extends:`, `supports:`, `criticizes:`, `source:`, `author:`) are not just labels that say "these notes are related." They are **operation contracts** that tell the agent what kind of traversal to perform and what to expect at the target. `extends:` expects a parent concept; `supports:` licenses evidence aggregation; `criticizes:` licenses contradiction detection; `source:` licenses grounding checks against the cited work.

**Practical consequence**: populate edge fields with the most specific type you can justify. Treat `related:` as a fallback for edges that don't yet have a specific semantic contract. Aggressive typing produces a more navigable knowledge graph than loose typing because each typed edge is an independent dimension for retrieval — unlike flat similarity where everything collapses to one scalar distance.

See `.claude/rules/typed-relationships.md` for the full edge vocabulary and the "Edges as Interface Operations" framing.

### Principle 3 — Hierarchical retrieval over flat search

Progressive disclosure through MOCs and sub-indexes is not a UI convenience; it is a **structural requirement for agent reliability** at scale. An agent navigating `VAULT-INDEX → MOC → concept → note` is operating outside the flat-retrieval regime where the Fano bound applies catastrophically. An agent running a single cosine-similarity query against the entire vault is inside that regime.

**Practical consequence**: build new material via hierarchical navigation paths. When creating a note, populate `up:` to place it in the hierarchy. When retrieving knowledge, prefer the indexed path (`obsidian search` from a MOC) over a flat content query.

### Where these principles come from

These are not ad-hoc design choices. They are grounded in a convergence of recent work on memory architectures for agents:

- **Formal theory**: The "no-escape theorem" (Barman et al., 2026, arXiv:2603.27116) proves that flat semantic retrieval over a finite-dimensional embedding space cannot simultaneously eliminate forgetting and false recall as memory grows. The only escape routes are (1) abandon meaning entirely, (2) add external symbolic grounding, or (3) make the semantic space infinite-dimensional (impossible for natural language). Typed hierarchical structure is option 2 realized.
- **Empirical validation**: xMemory (Hu et al., 2026, arXiv:2602.02007) demonstrates Pareto-dominant retrieval (48% fewer tokens with +21% F1 over flat RAG) via exactly this pattern: hierarchical decomposition, bounded branching, active consolidation. Appendix B of the paper derives the Fano bound ($n_k \leq 12$) formally.
- **Independent precursor**: Janowicz (2015, WOP keynote) articulated the pattern-based architecture — repositories with local ontologies linked through a shared pattern layer, with semantic signatures providing bottom-up structure discovery — a decade earlier, from ontology engineering practice.

The vault implements the engineering consequence: typed edges, bounded branching, hierarchical navigation, active curation. The `/audit` skill enforces the structural constraints; the `/curator` skill evolves the vocabulary; the knowledge graph makes the structure queryable.

**The short version of the short version**: flat search doesn't scale. Typed hierarchy does. This vault is built for typed hierarchy on purpose.

---

## How They Work Together

A typical interaction involves all four memory types:

```
You ask: "What do we know about topic X?"

1. Working memory (CLAUDE.md + rules) tells Claude HOW to navigate the vault
2. Procedural memory (/retrieve skill) tells Claude the STEPS for finding information
3. Semantic memory (VAULT-INDEX → MOC → notes) IS the knowledge Claude retrieves
4. Episodic memory (auto memory) may remind Claude "last time we discussed X, 
   the user preferred the framing from paper Y"
```

The `/encode` pipeline shows the reverse flow — creating new semantic memory:

```
You say: "Create a concept note about Y"

1. Working memory (rules) provides the type taxonomy and edge field vocabulary
2. Procedural memory (/encode skill) drives the pipeline: route → template → write → wire → verify
3. Episodic memory (Router memory) informs routing decisions from past corrections
4. Semantic memory (the new note) is the output — wired into MOCs, indexed, queryable
```

---

## Memory Consolidation: Auto Dream

Episodic memory accumulates noise over time — contradictory entries, stale debugging notes, relative dates that lose meaning. Claude Code's **Auto Dream** feature addresses this by running a consolidation cycle between sessions, analogous to REM sleep in biological memory systems.

Auto Dream runs automatically when two conditions are met: 24 hours since last consolidation AND 5+ sessions since last consolidation. It follows four phases:

1. **Orient** — read current memory directory, understand what exists
2. **Gather signal** — search session transcripts (JSONL) for corrections, decisions, recurring patterns
3. **Consolidate** — merge new signal into topic files, convert relative dates to absolute, delete contradicted facts, remove stale entries
4. **Prune and index** — update MEMORY.md to stay under 200 lines, remove stale pointers, add new ones

Check if Auto Dream is active: run `/memory` in a Claude Code session and look for "Auto-dream: on."

The vault's `/memory-audit` skill complements Auto Dream by providing manual audit capabilities: coverage testing (are high-frequency access patterns served by memory?), compression (shrink oversized files), and trajectory analysis (what files does the agent actually access most, measured from JSONL session logs).

See `03 - Resources/context/claude-code-auto-dream-docs.md` for the full Auto Dream documentation.

### The Longer Horizon: Weight Consolidation

Auto Dream consolidates within Phase 1 (external files). The deeper hypothesis: eventually, frequently-used procedural patterns will migrate from external context into model weights (Phase 2), freeing context budget and making those patterns intrinsic. This doesn't exist yet — but the vault's structured, inspectable Phase 1 memory is the right substrate for accumulating knowledge until Phase 2 consolidation becomes possible.

---

## Practical Implications

**For vault users:**
- Don't put everything in CLAUDE.md — it's working memory, keep it lean
- Skills are for procedures, not facts — if you're writing "always do X when Y," that's a rule or skill, not a vault note
- Daily notes are ephemeral by design — they're session journals, not permanent knowledge. Promote insights to concept notes via `/encode`
- The knowledge graph is free at rest — thousands of notes cost zero tokens until queried. Don't worry about vault size.

**For vault builders:**
- New behavioral guidance → rule file in `.claude/rules/`
- New workflow/procedure → skill in `.claude/skills/`
- New domain knowledge → vault note via `/encode`
- New personal preference → auto memory (Claude learns) or `owner-context.md` (you write)
- When in doubt about which memory type: ask "when should this be loaded?" Always → working memory (rule). On demand → procedural (skill). When relevant → semantic (vault note). Automatically → episodic (auto memory).

---

## For Reference

- [[Vault Architecture]] — Full structural reference for this vault
- [[How Progressive Disclosure Works]] — How working memory stays lean via layered navigation
- `03 - Resources/context/claude-code-memory-docs.md` — Official Claude Code memory system docs
- `03 - Resources/context/claude-code-skills-docs.md` — Official Claude Code skills system docs
- `03 - Resources/context/claude-code-extensions-docs.md` — When to use rules vs skills vs hooks
- `03 - Resources/context/claude-code-auto-dream-docs.md` — Auto Dream consolidation feature
