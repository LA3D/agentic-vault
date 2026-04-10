---
name: project-planning
description: "Create, plan, execute, and track projects in the vault. Use when starting a new project, creating PLAN.md files, defining phases and timelines, setting success criteria, archiving completed work, or organizing multi-week efforts in 01 - Projects/."
disable-model-invocation: false
---

# Project Planning Methodology

How to create, plan, execute, track, and archive projects in this vault.

---

## Principles

1. **Vault is source of truth** - All project planning lives in `01 - Projects/`
2. **Scale with complexity** - Single note for small work, full subfolder for multi-team efforts
3. **Cross-link everything** - Concepts, repos, Drive files, daily notes, literature
4. **PLAN.md for structured work** - Phased projects get a dedicated plan with timeline and success criteria
5. **Daily notes integrate** - Work log entries link to projects; don't maintain separate tracking
6. **Mirror to repos** - When repos exist, mirror relevant plan sections to repo README.md/CLAUDE.md
7. **Lifecycle tracking** - Projects move through states via `status` frontmatter

---

## Project Sizing

### Light (single note)

Solo tasks, small efforts, one-off work. Just a project note in `01 - Projects/` with tasks and links.

**Examples**: Blog post draft, one-week experiment, conference submission

### Standard (note + PLAN.md)

Multi-week work with phases. Project note + subfolder containing PLAN.md.

**Examples**: Grant proposal, course development, multi-week research experiment

### Complex (full structure)

Multi-team, multi-month efforts. Project note + subfolder with PLAN.md, sub-project plans, Decisions.md.

**Examples**: Industry partnerships, large grants, collaborative research programs

### Decision Tree

- Does it have phases or a timeline? → **Standard** (add PLAN.md)
- Multiple sub-projects or teams? → **Complex** (add sub-plans + Decisions.md)
- Otherwise → **Light** (single note)

---

## Project Creation Checklist

1. **Create project note** in `01 - Projects/[Name].md`
   - Add frontmatter: `status`, `timeline`, `tags`, `related` concepts
   - Write overview, goals, and initial tasks
2. **Determine sizing** using the decision tree above
3. **For Standard+**: Create subfolder `01 - Projects/[Name]/` with PLAN.md
4. **For Complex**: Add sub-project plans (`[Sub-Project]-PLAN.md`) and `Decisions.md`
5. **Place files in Google Drive** using the appropriate account
   - See `google-drive-navigation` skill for the decision tree
6. **Link to vault concepts** via wikilinks (`[[03 - Resources/...]]`)
7. **Update VAULT-INDEX.md** if the project is significant
8. **Commit to git** with descriptive message

---

## PLAN.md Pattern

Template for structured project plans:

```markdown
# [Project Name] - Plan

**Project**: [One-line description]
**Duration**: [Timeline]
**Status**: [Current phase]

---

## Project Overview

[2-3 sentences on what this project is and why it matters]

---

## Repositories

- Main: `~/dev/git/[org]/[repo]/`

---

## Timeline & Phases

### Phase 1: [Name] (Weeks X-Y)
- [ ] Week X: Task description
- [ ] Week Y: Task description

### Phase 2: [Name] (Weeks X-Y)
- [ ] Week X: Task description

---

## Key Decisions

- [ ] **[Decision]**: Options and context
- See [[Decisions]] for detailed decision log (Complex projects)

---

## Success Criteria

1. [What "done" looks like - deliverable 1]
2. [Deliverable 2]

---

## Links

### Vault Notes
- [[Project Note]] - Main project note
- Related concepts: [[Concept 1]], [[Concept 2]]

### Reference Documents
- [Doc name](file:///path/to/google/drive/file)

---

**Last Updated**: YYYY-MM-DD
**Next Review**: [When]
```

### Task Granularity Gate [NON-NEGOTIABLE]

When creating tasks in PLAN.md, each task must be completable in a single focused session. Vague tasks must be decomposed.

**Size targets**:
- Reading/review tasks: 2-5 minutes
- Research/synthesis tasks: 10-20 minutes
- Writing tasks: 15-30 minutes

**Decomposition example**:

Instead of:
```markdown
- [ ] Research context graphs
```

Write:
```markdown
- [ ] Read [[Context Graphs]] concept note (5 min)
- [ ] Query vault-kg for supporting literature (2 min)
- [ ] Read top 3 literature notes (15 min)
- [ ] Draft synthesis plan: thesis + source list (5 min)
```

**Research session integration**: Tasks can reference cognitive modes from the `research-session` skill:
```markdown
- [ ] Explore: context graphs — find 5+ sources (15 min)
- [ ] Architect: check taxonomy fit for new concept notes (10 min)
- [ ] Synthesize: architecture note from sources (20 min)
```

**Rationalization table**:

| Temptation | Why It's Wrong |
|------------|----------------|
| "Figure out details later" | Vague tasks don't get done — they get procrastinated. Decompose now. |
| "This project doesn't need a PLAN.md" | If it has phases or a timeline, it needs a plan. Check the sizing decision tree. |
| "Three phases is enough" | Phases are fine, but tasks within phases must be bite-sized. Decompose the tasks, not the phases. |

---

### Frontmatter for project notes

```yaml
---
created: YYYY-MM-DD
tags: [project, topic-tags]
status: planning  # planning | active | review | archived
timeline: [duration]
related:
  - "[[Related Concept]]"
---
```

---

## Vault <-> Repo Coordination

When a project has code repositories:

### Vault PLAN.md = source of truth
- All planning, timeline, and decision content lives in the vault
- Repo documentation mirrors relevant sections

### Mirror to repo README.md
- Copy project overview, timeline, and setup instructions
- Keep repo README focused on developers (build, run, test)
- Reference vault PLAN.md as authoritative source for full context

### Create repo CLAUDE.md
- Project context for Claude Code sessions in that repo
- Coding conventions, key files, architecture decisions
- Link back to vault PLAN.md:
  ```markdown
  ## Project Context
  **Full plan**: See `~/Obsidian/obsidian/01 - Projects/[Name]/PLAN.md`
  **Vault project note**: `01 - Projects/[Name].md`
  ```

### Sync is manual
- Copy relevant sections when plans change
- Automated mirroring is future work

---

## Cross-Tool Connections

How a project connects across the toolchain:

| Tool | Role | Location |
|------|------|----------|
| **Vault** | Planning, tracking, knowledge | `01 - Projects/[Name].md` + PLAN.md |
| **Google Drive** | Reference docs, shared files | `0 - Projects/[folder]/` (via `file://` URLs) |
| **Git repos** | Implementation code | `~/dev/git/[org]/[repo]/` |
| **Daily notes** | Work log entries | `Daily/YYYY-MM-DD.md` -> project wikilinks |
| **Research concepts** | Theory connections | `03 - Resources/` wikilinks |
| **Literature** | Papers and external sources | `03 - Resources/Literature/` links |

### Daily note integration

```markdown
# In Daily/YYYY-MM-DD.md

## Project Work
- Worked on [[Project Name]] Phase 2
- Implemented [feature] in `~/dev/git/org/repo/`
- Decision: chose [option] (see [[01 - Projects/Name/Decisions]])
```

---

## Project Lifecycle States

Track via `status` frontmatter field in the project note:

| State | Meaning | Action |
|-------|---------|--------|
| `planning` | Scoping, initial setup | Create note + PLAN.md |
| `active` | Work in progress | Daily note links, task updates |
| `review` | Wrapping up, evaluating outcomes | Document results, lessons learned |
| `archived` | Complete or paused | Move to `04 - Archive/`, update VAULT-INDEX |

### Transitions
- `planning` -> `active`: When first real work begins
- `active` -> `review`: When deliverables are complete or deadline passes
- `review` -> `archived`: After retrospective, lessons captured
- Any state -> `archived`: If project is cancelled or indefinitely paused

### Archival process
1. Update `status: archived` in frontmatter
2. Move project note and subfolder to `04 - Archive/`
3. Remove from VAULT-INDEX.md active projects section
4. Archive corresponding Google Drive folder

---

## Integration with Existing Workflows

- **Tasks**: See `.claude/rules/task-management.md` — project notes remain the source of truth for task lists
- **Research**: See `.claude/rules/research-workflows.md` — projects can have "Research Connections" sections linking to `03 - Resources/`
- **Linking**: See `.claude/rules/linking-guide.md` — bidirectional links between project and concept notes
- **Google Drive**: See `google-drive-navigation` skill — file placement decision tree
- **Daily notes**: Morning: surface project tasks. Evening: update progress and commit.

---

## Example: Multi-Phase Research Project (Complex)

```
01 - Projects/
├── Collaborative AI Research Platform.md           # Project note (frontmatter + overview)
└── Collaborative AI Research Platform/
    ├── PLAN.md                                     # Master plan (timeline, phases, criteria)
    ├── Data-Pipeline-PLAN.md                       # Sub-project plan
    ├── Evaluation-Framework-PLAN.md                # Sub-project plan
    └── Decisions.md                                # Decision log
```

- Project note has `status: active`, `timeline: 12 weeks`
- PLAN.md links to vault concepts (`[[Knowledge Graphs]]`, `[[Evaluation Metrics]]`, `[[Agent Architecture]]`)
- Google Drive files linked via `file://` URLs
- Repos (when created) will get mirrored README.md + CLAUDE.md
