# CLAUDE.md

This file provides guidance to Claude Code when working with this Obsidian vault.

## Owner

> **First time?** Run `/onboarding` to populate this section. The onboarding skill will interview you and configure the vault for your context.

**See**: `.claude/rules/owner-context.md` for full context (populated during onboarding)

---

## Vault Overview

A **linked knowledge system** organized around Areas of Focus (Pullein/GAPRA framework). Areas are the foundation — every project, MOC, and task should connect back to an area. The vault handles the *knowledge dimension* of each area.

**Areas of Focus** (`02 - Areas of Focus/`): Defined during onboarding. See `[[Areas of Focus - Pullein Methodology]]`.

**Architecture**: See `[[Vault Architecture]]` for the full structural reference.

---

## Navigation [CRITICAL]

**Read VAULT-INDEX.md** at session start for routing to sub-indexes and MOCs.

**Progressive disclosure**: VAULT-INDEX (routing) → Sub-indexes/MOCs (domain) → Individual notes (detail). See `[[How Progressive Disclosure Works]]`.

**CLI-first**: When the Obsidian app is running, prefer `obsidian search`, `obsidian backlinks`, `obsidian tags` over grep for vault queries. See `.claude/rules/vault-navigation.md`.

---

## Vault Structure

```
/
├── 02 - Areas of Focus/        # THE FOUNDATION — your areas (Pullein)
├── 01 - Projects/              # Time-bound efforts serving areas
├── 03 - Resources/             # Knowledge organized by topic (MOCs)
│   ├── Literature/             # Paper notes + LITERATURE-INDEX.md
│   ├── Obsidian Reference/     # Vault management guides + how-it-works docs
│   └── [your topic folders]/   # Created as your vault grows
├── 04 - Archive/               # Inactive items
├── 05 - Watching/              # Monitored items not yet committed to (fleeting notes)
├── Daily/                      # Daily notes (YYYY-MM-DD.md)
├── Inbox/                      # Unsorted notes (processing queue)
├── Templates/                  # Note templates (7 types)
└── scripts/                    # Helper scripts (KG pipeline)
```

**Hierarchy**: Areas → Goals → Projects → Tasks. Every project should connect to an area via the `area:` edge field.

**Watching folder** (`05 - Watching/`): For items being monitored but not yet committed to — funding opportunities, emerging projects, things flagged for attention. Use `type: fleeting-note` with `status: watching`. When resolved: promote to `01 - Projects/` or archive to `04 - Archive/`. Do NOT put fleeting notes in `Inbox/` — Inbox is a processing queue, not a home.

---

## Git Protocol [CRITICAL]

```bash
git add [specific-files]
git commit -m "$(cat <<'EOF'
[Agent: Claude] Brief description

- List specific modifications

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**Never**: force push to main, skip hooks, use `git add -A`, commit without descriptive messages.

---

## Note Typing and Typed Relationships

All new notes must include `type:` in frontmatter. Use edge fields (`up:`, `area:`, `concept:`, `source:`, `extends:`, `supports:`, `criticizes:`) for typed relationships. These fields define the vault's knowledge graph — consumed by the KG pipeline (`scripts/kg/`) for SPARQL queries and by Claude Code for navigation. When creating projects or MOCs, populate `area:` to connect them to an area of focus.

**See**: `.claude/rules/typed-relationships.md` for the full taxonomy

---

## Rules (always loaded — `.claude/rules/`)

| Rule | Covers |
|------|--------|
| `vault-navigation.md` | CLI-first navigation, progressive disclosure, health checks |
| `typed-relationships.md` | Type taxonomy, edge fields, KG vocabulary, template patterns |
| `linking-guide.md` | Wikilink conventions, code-to-vault linking, MOC strategy |
| `task-management.md` | Task discovery (CLI + grep), daily workflow, Tasks plugin |
| `research-workflows.md` | Research sessions, navigation patterns |
| `owner-context.md` | Your background, projects, affiliations, preferences |
| `discipline-gates.md` | Cross-skill gates, universal rationalizations, gate types |

## Skills (loaded on demand — `.claude/skills/`)

### Core Vault Skills
| Skill | Invoke | Covers |
|-------|--------|--------|
| `onboarding` | `/onboarding` | First-time setup: interview, areas, namespace, dev path |
| `encode` | `/encode`, `/wire` | Note creation + wiring for all vault domains |
| `retrieve` | `/retrieve` | Structured retrieval into working memory |
| `review-note` | `/review-note` | Two-stage gated note review (structural → quality) |
| `audit` | `/audit` | Vault structural health check |
| `vault-curator` | `/curator` | Ontology governance: review suggestions, evolve vocabulary |
| `vault-kg` | `/vault-kg` | Knowledge graph queries, semantic navigation |
| `project-planning` | `/project-planning` | Project sizing, PLAN.md pattern |
| `research-session` | `/research-session` | Structured research with 5 cognitive modes |
| `session-retro` | `/session-retro` | End-of-session reflection and daily note handoff |
| `obsidian-research-synthesis` | `/obsidian-research-synthesis` | Design-gated synthesis from 3+ vault sources |
| `obsidian-knowledge-capture` | `/obsidian-knowledge-capture` | Identify knowledge worth capturing → delegates to Encode |
| `obsidian-spec-to-implementation` | `/obsidian-spec-to-implementation` | Spec → implementation tasks breakdown |
| `memory-audit` | `/memory-audit` | Audit Claude's memory files for quality |

### Recommended Free Integrations
| Skill | Invoke | Covers | Setup |
|-------|--------|--------|-------|
| `alphaxiv-paper-lookup` | `/alphaxiv-paper-lookup` | ArXiv paper lookup via summaries | None — uses web |
| `notebooklm` | `/notebooklm` | Google NotebookLM API | Google account |
| `quarto` | `/quarto` | Render documents to PDF/HTML/slides | `brew install --cask quarto` |

### Optional Paid Integrations (not shipped — install separately)
See `[[Integration Ecosystem]]` for setup guides, free alternatives, and what each tool adds.

| Tool | What it adds | Free alternative |
|------|-------------|-----------------|
| Readwise ($8/mo) | Automatic highlight sync from Kindle, web, podcasts | Manual capture via `/encode` |
| Todoist ($4/mo) | Task management with time sectors | Obsidian Tasks plugin (free) |
| Paperpile ($3/mo) | Reference management + Google Docs integration | Zotero (free, open source) |

---

## Cross-Repo Workflow

This vault works alongside your code projects. Two key patterns:

**Two-level planning**: Vault-level plans (`01 - Projects/PLAN.md`) are strategic — research questions, goals, area connections. Repo-level plans (in git repos) are tactical — implementation, architecture. Use `/project-planning` in both contexts.

**The `--add-dir` bridge**: When working in a git repo, run `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir /path/to/this/vault` so Claude Code can reference vault knowledge AND load this CLAUDE.md + rules. Without the env var, `--add-dir` gives file access but doesn't load vault instructions.

**Building new skills**: Use Anthropic's built-in `/skill-creator` to build domain-specific skills. Domain skills make domain decisions → delegate note creation to `/encode`.

---

## Quick Reference

- **Areas of Focus**: `02 - Areas of Focus/` — your foundational areas
- **Vault architecture**: `03 - Resources/Obsidian Reference/Vault Architecture.md`
- **Vocabulary**: `03 - Resources/Obsidian Reference/Vault Vocabulary.md` — canonical types and edges
- **Integration options**: `03 - Resources/Obsidian Reference/Integration Ecosystem.md`
- **Style guides**: `03 - Resources/context/` (optional — AI-ese avoidance, coding style)
