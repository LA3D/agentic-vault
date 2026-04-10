# Agentic Vault

A shareable vault template for building an **agentic memory system** with Claude Code and Obsidian. Ships with PARA structure, typed relationships, a knowledge graph pipeline, and 14+ skills that let Claude Code navigate, create, review, and maintain your knowledge base.

## What This Is

This vault implements a cognitive architecture where:
- **You** provide direction, domain judgment, and raw input
- **Claude Code** structures, cross-links, and maintains the knowledge
- **The vault** is the persistent shared memory between sessions

The structure is based on the Pullein/GAPRA framework (Areas → Goals → Projects → Tasks) with typed frontmatter relationships that form a queryable knowledge graph.

## Quick Start

### 1. Clone and open

```bash
git clone https://github.com/LA3D/agentic-vault.git ~/Obsidian/my-vault
cd ~/Obsidian/my-vault
```

Open the folder as a vault in Obsidian.

### 2. Run onboarding

```bash
claude
# Then in the Claude Code session:
# /onboarding
```

The onboarding skill will:
- Interview you (name, role, expertise, preferences)
- Help you define your areas of focus
- Ask for your knowledge graph namespace
- Configure your dev environment path

### 3. Start working

Create your first project, capture a concept, or start a research session:
- `/encode` — create any type of note
- `/project-planning` — start a new project
- `/research-session` — structured deep dive on a topic

## Dependency Tiers

The vault works at any tier. Higher tiers add capabilities.

| Tier | What | Install |
|------|------|---------|
| **0 — Essential** | Git, Claude Code | Required |
| **1 — Core vault** | Obsidian | `brew install --cask obsidian` |
| **2 — Knowledge graph** | Python 3 + PyYAML, Apache Jena | `brew install jena && pip install pyyaml` |
| **3 — Fast search** | Obsidian CLI | Built into Obsidian 1.12+. Settings > General > CLI |
| **4 — Google integration** | GWS skills | Google account + API setup (see [Integration Ecosystem](03%20-%20Resources/Obsidian%20Reference/Integration%20Ecosystem.md)) |
| **5 — Premium tools** | Readwise, Todoist, etc. | Optional paid subscriptions (free alternatives documented) |

### Installing Tier 2 (Knowledge Graph)

```bash
# macOS (Homebrew)
brew install jena
pip install pyyaml

# Configure your namespace (run once)
scripts/kg/setup-namespace.sh https://yourdomain.com/vault
# Or keep the default: https://example.com/vault

# Build the graph
scripts/kg/build-graph.sh --stats
```

### Installing Tier 3 (Obsidian CLI)

1. Open Obsidian
2. Settings > General > Command line interface > Enable
3. Verify: `obsidian help`

## Vault Structure

```
├── CLAUDE.md                    # Claude Code's orientation (reads this first)
├── VAULT-INDEX.md               # Top-level routing table
├── .claude/
│   ├── rules/                   # 7 behavioral rules (loaded every session)
│   └── skills/                  # 14+ on-demand capabilities
├── Templates/                   # 7 note templates
├── 01 - Projects/               # Time-bound efforts
├── 02 - Areas of Focus/         # Your foundational life areas
├── 03 - Resources/              # Knowledge by topic (MOCs)
├── 04 - Archive/                # Completed/inactive items
├── 05 - Watching/               # Monitored items
├── Daily/                       # Daily notes
└── scripts/kg/                  # Knowledge graph pipeline
```

## Key Concepts

- **Progressive Disclosure**: Claude navigates in layers (VAULT-INDEX → MOC → note), not by reading everything. See [How Progressive Disclosure Works](03%20-%20Resources/Obsidian%20Reference/How%20Progressive%20Disclosure%20Works.md).

- **Typed Relationships**: Frontmatter edge fields (`up:`, `concept:`, `source:`, `extends:`, etc.) create a knowledge graph that Claude can query via SPARQL. See [Vault Vocabulary](03%20-%20Resources/Obsidian%20Reference/Vault%20Vocabulary.md).

- **Two-Level Planning**: Vault-level plans are strategic (goals, research questions). Repo-level plans are tactical (implementation). Bridge them with `claude --add-dir /path/to/vault`.

- **The Encode Pipeline**: All note creation goes through `/encode`, which routes to the right location, applies the right template, wires into MOCs, and verifies before committing.

## Core Skills

| Skill | Purpose |
|-------|---------|
| `/onboarding` | First-time vault setup |
| `/encode` | Create and wire any note type |
| `/retrieve` | Load related notes into context |
| `/review-note` | Quality review with specialist agents |
| `/audit` | Vault-wide structural health check |
| `/vault-kg` | SPARQL queries on the knowledge graph |
| `/research-session` | Structured 5-mode research deep dive |
| `/session-retro` | End-of-session reflection |
| `/project-planning` | Project sizing and PLAN.md creation |

## Building Your Own Skills

Use Anthropic's built-in `/skill-creator` to build domain-specific skills for your work. The pattern: your domain skill handles domain decisions → delegates note creation to `/encode`. See the existing skills in `.claude/skills/` for examples.

## Cross-Repo Workflow

When working in a git repo, give Claude access to your vault:

```bash
# One-time alias (add to .bashrc/.zshrc)
alias cc='claude --add-dir ~/Obsidian/my-vault'

# Then in any git repo:
cc
```

This lets Claude reference vault knowledge (concept notes, literature, project plans) while implementing code.

## Integration Options

The vault is a central processing hub. External tools feed information in. See [Integration Ecosystem](03%20-%20Resources/Obsidian%20Reference/Integration%20Ecosystem.md) for the full menu of free and paid options at each integration point.

## License

MIT
