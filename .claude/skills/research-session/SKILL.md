---
name: research-session
description: "Use when user says 'research session', 'let's explore X', 'deep dive on X', 'research mode', or at start of extended research work block"
---

# Research Session

Structure extended research work with explicit cognitive modes. Prevents hyperfocus drift, ensures all research work ends with committed, linked knowledge.

**Usage**: `/research-session [topic]` or natural triggers ("let's explore X", "deep dive on X", "research mode")

---

## Session Initialization

1. **Announce**: "Starting research session on [topic]"
2. **Set anchor**: Identify the relevant MOC and project note
3. **Check existing coverage**: Query vault for what we already know

```bash
obsidian search vault="obsidian" query="[topic]" limit=15
```

4. **Propose starting mode**: Usually Explore, unless user has specific intent

---

## Five Cognitive Modes

### Mode 1: Explore (Divergent)

**Gear**: Cast wide net. Follow connections. No filtering.

**Behavior**:
- Use `/retrieve targeted` or `/retrieve contextual` for structured vault context loading (returns a manifest with reading order and budget tracking)
- Use `vault-kg` for custom graph queries beyond Retrieve's built-in modes
- Use WebFetch / `defuddle` for external sources
- Use `alphaxiv-paper-lookup` for paper discovery
- Use `/retrieve exploratory` to find unexpected connections and underexplored notes
- Create `fleeting-note` entries in `05 - Watching/` for ideas worth monitoring
- No quality gates — volume and breadth matter here

**Time-box suggestion**: ~15 minutes. Agent suggests transition when Explore runs long.

**Transition to Architect when**: You have enough raw material (5+ relevant sources identified).

---

### Mode 2: Architect (Structural)

**Gear**: Check taxonomy fit. Organize what was found.

**Behavior**:
- Review what Explore found against the vault's type taxonomy
- Check if existing MOCs cover the territory or if new structure is needed
- Run `vault-curator` health checks on the relevant area if useful
- Identify which fleeting notes should become typed notes
- Map sources to canonical types (literature-note, concept-note, external-resource, etc.)
- Identify gaps: what's missing that we'd need for a synthesis?

**Time-box suggestion**: ~10 minutes.

**Transition to Synthesize when**: Sources are organized and gaps are identified.

---

### Mode 3: Synthesize (Integrative)

**Hard Gate**: Must have 3+ source notes from Explore/Architect phases before entering this mode. If fewer than 3, return to Explore.

**Gear**: Build arguments. Create theory/concept notes.

**Behavior**:
- Invoke `obsidian-research-synthesis` for structured synthesis
- Follow the synthesis skill's design gate (plan → approve → execute)
- Create typed notes with proper edge field frontmatter
- Attribute every claim to a source via wikilink
- Update MOCs with new entries

**Time-box suggestion**: ~20 minutes.

**Transition to Critique when**: Synthesis notes are drafted.

---

### Mode 4: Critique (Adversarial)

**Hard Gate**: Must have synthesized notes to review. Cannot enter this mode with nothing to critique.

**Gear**: Stress-test. Find gaps. Challenge assumptions.

**Behavior**:
- Invoke `review-note --final` on each synthesized note
- Check for unsupported claims, missing sources, conceptual drift
- Verify structural compliance (frontmatter, edge fields, links)
- Flag AI-ese patterns
- Identify what the synthesis gets wrong or overstates

**Time-box suggestion**: ~10 minutes.

**Transition to Ship when**: All synthesized notes pass review (or issues are fixed).

---

### Mode 5: Ship (Convergent)

**Hard Gate**: Must have passed Critique on all synthesized notes. Cannot ship unreviewed work.

**Gear**: Commit. Close out. Create handoff.

**Behavior**:
1. Commit all new/modified files with descriptive messages
2. Update MOCs and indexes with new entries
3. Update the project note with progress
4. Write session summary for the daily note:

```markdown
## Research Session: [Topic]

**Duration**: ~[X] minutes
**Mode progression**: Explore → Architect → Synthesize → Critique → Ship

### Created
- [[New Note 1]] (type) — [one-line summary]
- [[New Note 2]] (type) — [one-line summary]

### Updated
- [[Existing Note]] — [what changed]
- [[MOC Name]] — added [N] entries

### Open Threads
- [Topic needing more exploration]
- [Question not yet answered]

### Next Session
- Start in [mode] with [specific focus]
```

5. Append session summary to daily note

---

## Mode Transitions

**Explicit announcements required.** Before switching modes:

1. State: "Transitioning from [current mode] to [next mode]"
2. State reason: "Because [rationale — e.g., 'we have enough sources to synthesize']"
3. If skipping a mode, explain why

**Agent suggests transitions** when:
- A mode has run past its time-box suggestion
- A gate condition for the next mode is met
- The user seems stuck or drifting

**User can override**: "Stay in Explore" or "Skip to Ship" are valid commands. But the agent should flag if a gate isn't met (e.g., "We don't have 3+ sources yet for Synthesize — continue Exploring or proceed anyway?").

---

## ADHD Accommodations

- **Time-box suggestions** prevent hyperfocus in Explore mode (the most common trap)
- **Explicit mode names** externalize the cognitive gear-shift that's hard to do internally
- **Ship mode is mandatory** — sessions always end with committed work, not open tabs
- **Session summary creates a handoff** so the next session starts with context, not from scratch
- **"Good enough" over perfect**: Critique mode checks for errors, not perfection

---

## Rationalization Table

| Temptation | Why It's Wrong |
|------------|----------------|
| "Just a bit more exploring" | Explore mode is the hyperfocus trap. Check: do you have 5+ sources? If yes, move to Architect. |
| "I'll skip Architect, straight to Synthesize" | Architect catches taxonomy mismatches before you embed them in synthesis notes. Take 10 minutes. |
| "Don't need 3 sources" | Synthesis from <3 sources is paraphrasing, not synthesis. Go find more. |
| "Critique can wait" | Post-hoc review costs more than inline. Do it now while the synthesis is fresh. |
| "I'll commit later" | Ship mode exists because uncommitted work is lost work. Commit now. |
| "No need for a session summary" | The summary is the handoff. Without it, the next session starts cold. |

---

## Red Flags — STOP

- Spending >30 minutes in Explore without transitioning
- Entering Synthesize with fewer than 3 source notes
- Shipping notes that haven't passed Critique
- Ending a session without entering Ship mode
- Creating notes without updating MOCs/indexes

---

## Related Skills

- **obsidian-research-synthesis**: Called during Synthesize mode
- **review-note**: Called during Critique mode
- **retrieve**: Primary context-loading tool during Explore mode (structured manifests with budget tracking)
- **vault-kg**: Used during Explore and Architect for custom SPARQL queries beyond Retrieve's modes
- **vault-curator**: Used during Architect mode for health checks
- **session-retro**: Can be invoked at session end for deeper reflection
