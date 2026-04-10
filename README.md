# Agentic Vault

A shareable vault template for building an **agentic memory system** with Claude Code and Obsidian. Ships with PARA structure, typed relationships, a knowledge graph pipeline, and 14+ skills that let Claude Code navigate, create, review, and maintain your knowledge base.

## What This Is

This vault implements a cognitive architecture where:
- **You** provide direction, domain judgment, and raw input
- **Claude Code** structures, cross-links, and maintains the knowledge
- **The vault** is the persistent shared memory between sessions

### Why PARA?

The vault uses a modified [PARA](https://fortelabs.com/blog/para/) system (Projects, Areas, Resources, Archive) because it gives Claude Code unambiguous routing rules for every piece of information. The `/encode` skill's Router maps note types to PARA categories automatically — a concept note goes in Resources, a project plan goes in Projects, a fleeting thought goes in Watching.

On top of PARA, we layer Carl Pullein's Areas of Focus framework: your 6-8 foundational life/work areas become the *strategic layer* that everything else connects to. Every project should serve an area. This connection is enforced by the Router, the `/audit` skill, and SHACL validation in the knowledge graph.

We also add a **Watching** folder (`05 - Watching/`) for items you're monitoring but haven't committed to — a staging area between "interesting" and "active."

See [Why PARA and How We Modify It](03%20-%20Resources/Obsidian%20Reference/Why%20PARA%20and%20How%20We%20Modify%20It.md) for the full rationale, including how the Router enforces the structure.

## Prerequisites

You need three things before starting. Install them in order:

### 1. Homebrew (macOS package manager)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Core tools
```bash
brew install git node ripgrep gh
brew install --cask obsidian
```

### 3. Claude Code

Claude Code is Anthropic's agentic coding tool — it's the AI agent that operates inside this vault. You need an **Anthropic account with a paid plan** (the [Max plan](https://www.anthropic.com/pricing) at $100/mo includes Claude Code usage; alternatively, pay per-token via the [API console](https://console.anthropic.com)).

```bash
# Install the CLI
npm install -g @anthropic-ai/claude-code

# Authenticate (follow the prompts)
claude
```

Claude Code is also available as a [VS Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code), [JetBrains plugin](https://plugins.jetbrains.com/plugin/claude-code), [desktop app](https://claude.ai/download), or [web app](https://claude.ai/code). The CLI is recommended for this vault because skills work best in the terminal.

> **See [SETUP.md](SETUP.md) for the full setup guide** — additional tiers of tools (knowledge graph pipeline, Quarto, Google Workspace integration) that Claude Code can help you install during onboarding.

---

## Quick Start

> **This is a GitHub template repository.** Don't clone it directly — use it to create your own repo. This keeps your vault independent with its own git history, and you won't accidentally push to the template.

### 1. Create your vault from the template

**Option A — GitHub web UI:**
Click the green **"Use this template"** button at the top of this repo → "Create a new repository." Choose your own account/org, name it whatever you like (e.g., `my-vault`, `research-vault`, `knowledge-base`), and set it to private.

**Option B — GitHub CLI:**
```bash
gh repo create my-vault --template LA3D/agentic-vault --private --clone
cd my-vault
```

### 2. Choose where to put it

Obsidian supports multiple vaults — each vault is just a folder. A common convention is a dedicated directory:

```bash
# If you used Option A (web UI), clone your new repo:
git clone git@github.com:YOUR-USERNAME/my-vault.git ~/Obsidian/my-vault

# If you used Option B (CLI), it's already cloned. Move it if you like:
mv my-vault ~/Obsidian/my-vault
```

> **Multiple vaults**: You can have separate vaults for different purposes — a research vault, a work vault, a personal vault. Each is an independent git repo. Obsidian lets you switch between them. Claude Code's `--add-dir` flag lets you reference one vault while working in another.

### 3. Open in Obsidian

Open Obsidian → "Open folder as vault" → select your vault directory. When prompted about community plugins, enable them (the vault uses Templater, Dataview, and Tasks).

### 4. Run onboarding

```bash
cd ~/Obsidian/my-vault
claude
# Then in the Claude Code session:
# /onboarding
```

The onboarding skill will:
- Check your installed tools and suggest what to add (see [SETUP.md](SETUP.md))
- Interview you (name, role, expertise, preferences)
- Help you define your areas of focus
- Ask for your knowledge graph namespace
- Configure your dev environment path

### 5. Start working

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
