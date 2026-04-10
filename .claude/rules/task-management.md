# Task Management Workflow

How Claude Code discovers, creates, updates, and tracks tasks across the vault.

---

## Principles

1. **Areas are the foundation** — every task should ultimately serve an area of focus (Pullein/GAPRA). If a task doesn't connect to an area, question why you're doing it.
2. **Hierarchy**: Areas → Goals → Projects → Tasks. Tasks live in project notes; projects serve areas.
3. **Tasks live where they belong** — in project notes, daily notes, or area notes for recurring routines
4. **Project notes are source of truth** — `01 - Projects/` holds canonical task lists
5. **Markdown checkboxes** — `- [ ]` / `- [x]` syntax, no proprietary format
6. **Projects provide structure** — invoke `/project-planning` skill for PLAN.md patterns

---

## Task Discovery

### CLI-first (preferred)

```bash
obsidian tasks todo                          # All open tasks vault-wide
obsidian tasks todo path="01 - Projects"     # Project tasks only
obsidian tasks todo daily                    # Daily note tasks
obsidian task ref="path:line" done           # Mark complete via CLI
```

### Grep fallback (Obsidian not running)

```bash
grep -rn "- \[ \]" "01 - Projects/"         # Project tasks
grep -rn "- \[ \]" --include="*.md" .        # Vault-wide
```

For general CLI reference, see [vault-navigation.md](vault-navigation.md).

---

## Task Creation

1. Find the relevant project in `01 - Projects/`
2. Add task in "Next Steps" section with wikilinks: `- [ ] Task ([[Related Concept]])`
3. Or via CLI: `obsidian daily:append content="- [ ] Task description"`

---

## Task Updates

Complete tasks with the Edit tool: change `- [ ]` to `- [x]` in the source file.

Optionally note completions in the daily note linking back to the project.

---

## Daily Workflow

**Morning**: Review area notes for recurring routines → read project notes for open tasks → create daily note with today's focus. Pullein: plan no more than 50% of your time; keep flexibility for the unexpected.
**During work**: Update task status, add new tasks, link to concepts/implementations
**Evening**: Summarize in daily note, move unfinished tasks, commit. (Pullein recommends evening planning for the next day — hit the ground running.)

### Daily Note Sections

```markdown
# YYYY-MM-DD

## Today's Focus
- [ ] Task from [[Project A]] (serves [[Research & Scholarship]])

## Research Work / Papers Read
(wikilinks to concepts, literature, repos)

## Routines
- [ ] Recurring routine from [[Health & Wellness]]

## Completed
- [x] Done task ([[Project]])
```

### Weekly Quick-Scan

Once a week, scan each area of focus: am I doing *something* for each area? Review `02 - Areas of Focus/` area notes and their "Current Goals" sections. Move tasks into this week's focus.

### Six-Month Deep Review

Review each area note: redefine standards, assess goal progress, update the Reflection Log. Simplify — remove routines that aren't serving you, add new ones that would. See [[Areas of Focus - Pullein Methodology]].

---

## Obsidian Tasks Plugin

The vault has the Tasks plugin. Use query blocks in notes:

```markdown
\`\`\`tasks
not done
path includes 01 - Projects
\`\`\`
```

These render dynamically and pull tasks from across the vault.

---

**Related**:
- [vault-navigation.md](vault-navigation.md) — CLI commands and navigation
- [linking-guide.md](linking-guide.md) — How to link tasks to concepts
- [typed-relationships.md](typed-relationships.md) — `area:` edge field connects projects to areas
- `[[Areas of Focus - Pullein Methodology]]` — GAPRA framework and review cadences
