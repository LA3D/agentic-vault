# Setup Guide

Detailed setup instructions for the agentic vault, organized by dependency tier. See the [README](README.md) for a quick start.

> **The onboarding skill (`/onboarding`) will check which tools are installed and guide you through what's missing.** You don't need to install everything upfront — start with Tier 0 and add capabilities as you need them.

---

## Tier 0 — Essential (required)

These are non-negotiable. The vault doesn't function without them.

### Homebrew (macOS package manager)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Git
```bash
brew install git
```

### Claude Code

Claude Code is Anthropic's agentic coding tool — it's the agent that operates inside this vault. It reads your files, creates notes, runs skills, and manages the knowledge graph. You need two things:

**1. An Anthropic account with API access**

Sign up at https://console.anthropic.com. You'll need a paid plan (Pro or Team) — Claude Code uses the API, which requires billing. The Max plan ($100/mo) includes Claude Code usage directly; otherwise you pay per-token via the API.

**2. Install Claude Code**

The recommended install is the CLI:

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Verify
claude --version
```

See https://claude.com/product/claude-code for full install documentation.

Claude Code is also available as:
- **VS Code extension** — search "Claude Code" in the extensions marketplace
- **JetBrains extension** — search "Claude Code" in the plugin marketplace  
- **Desktop app** (macOS/Windows) — download from https://claude.ai/download
- **Web app** — https://claude.ai/code

The CLI is recommended for this vault because skills (`/encode`, `/onboarding`, etc.) work best in the terminal.

**3. Authenticate**

```bash
claude
# Follow the prompts to log in with your Anthropic account
```

Once authenticated, Claude Code stores credentials locally. You won't need to log in again on this machine.

### Obsidian
```bash
brew install --cask obsidian
```

After installing, open this folder as a vault in Obsidian.

---

## Tier 1 — Core CLI Tools (strongly recommended)

These make Claude Code significantly more effective. Install them all at once:

```bash
brew install ripgrep gh jq bat pandoc
brew install --cask quarto
```

| Tool | What it does | Why it matters |
|------|-------------|----------------|
| **ripgrep** (`rg`) | Fast regex search | Claude Code's Grep tool uses this under the hood |
| **gh** | GitHub CLI | Create repos, PRs, issues from the terminal |
| **jq** | JSON processor | Query and transform JSON (used by KG pipeline, API responses) |
| **bat** | Syntax-highlighted cat | Better file viewing in terminal |
| **Quarto** | Document rendering (PDF, HTML, slides, DOCX) | The `/quarto` skill uses this to produce publication-quality output from vault content. Free and open source. |
| **Pandoc** | Document format conversion | Lower-level converter that Quarto builds on. Also useful standalone for quick format conversions. |

---

## Tier 2 — Knowledge Graph Pipeline (recommended)

Enables SPARQL queries on your vault's knowledge graph — multi-hop concept traversal, orphan detection, hub analysis.

### Python 3 + PyYAML
```bash
brew install python3
pip install pyyaml
```

The KG pipeline script (`scripts/kg/vault-to-jsonld.py`) only needs stdlib + PyYAML. No rdflib required.

### Apache Jena
```bash
brew install jena
```

This installs three tools:
- **`arq`** — SPARQL query engine (the main one you'll use)
- **`riot`** — RDF format converter (JSON-LD → Turtle)
- **`shacl`** — SHACL validation (checks graph integrity)

### Verify
```bash
arq --version    # Should show Apache Jena
riot --version
python3 -c "import yaml; print('PyYAML OK')"
```

### Configure namespace and build
```bash
# Set your namespace (or keep the default)
scripts/kg/setup-namespace.sh https://yourdomain.com/vault

# Build the graph (will be empty in a fresh vault — that's fine)
scripts/kg/build-graph.sh --stats
```

---

## Tier 3 — Obsidian CLI (recommended)

Built into Obsidian 1.12+. Provides indexed search that's 54x faster than grep.

1. Open Obsidian
2. Settings → General → Command line interface → **Enable**
3. Follow the instructions to add it to your PATH

### Verify
```bash
obsidian help
obsidian search query="test" limit=5
```

**If Obsidian isn't running**, the CLI won't work. Claude Code falls back to grep/Glob automatically.

---

## Tier 4 — Node.js Ecosystem (recommended for skills)

Required for installing additional Claude Code skills from the marketplace and for some skill tools.

```bash
brew install node
```

### Skill management
```bash
# Install the skill finder (discovers and installs community skills)
npx @anthropic-ai/claude-code-skills find-skills

# Install Google Workspace skills
npx @anthropic-ai/claude-code-skills install gws
```

### Useful npm tools
```bash
npm install -g defuddle-cli    # Clean web page extraction (strips navigation/clutter)
```

---

## Tier 5 — Google Workspace Integration (recommended, free)

Requires a Google account and API setup. Gives Claude Code access to Gmail, Calendar, Drive, Docs, Sheets.

### Setup steps
1. Create a Google Cloud project at https://console.cloud.google.com
2. Enable the APIs you need (Gmail, Calendar, Drive, etc.)
3. Create OAuth 2.0 credentials
4. Install the GWS skills: `npx @anthropic-ai/claude-code-skills install gws`
5. Authenticate: `gws auth login`

The `gws-shared` skill has detailed setup instructions. Run `/gws-shared` in Claude Code for a walkthrough.

---

## Tier 6 — Premium Integrations (optional, paid)

These accelerate specific workflows. Free alternatives exist for each — see [[Integration Ecosystem]].

### Readwise (~$8/mo)
Automatic highlight sync from Kindle, web, podcasts.
- Install the Readwise Official Obsidian plugin (Settings → Community plugins)
- Install the processing skill separately (not included in template)

### Todoist (~$4/mo)
Task management with projects, labels, priorities.
```bash
npm install -g @doist/todoist-cli
td login
```

### Paperpile (~$3/mo)
Reference management with Google Docs integration. Alternative: **Zotero** (free, open source).

---

## Recommended Brewfile

For a complete one-command setup of Tiers 0-2 plus useful tools:

```bash
# Save as Brewfile, then run: brew bundle
# Tier 0 — Essential
brew "git"
cask "obsidian"
# Tier 1 — Core CLI tools
brew "ripgrep"
brew "gh"
brew "jq"
brew "bat"
brew "pandoc"
cask "quarto"
# Tier 2 — Knowledge Graph
brew "jena"
# Tier 4 — Node.js ecosystem
brew "node"
# Useful extras
brew "tree"
brew "fzf"
```

```bash
# Install everything
brew bundle

# Then Python deps
pip install pyyaml
```

---

## Verifying Your Setup

The `/onboarding` skill checks for installed tools automatically. You can also run this manually:

```bash
echo "=== Tier 0 ==="
which git && echo "✓ git" || echo "✗ git"
which claude && echo "✓ claude" || echo "✗ claude (Claude Code)"
which obsidian && echo "✓ obsidian" || echo "✗ obsidian"

echo "=== Tier 1 ==="
which rg && echo "✓ ripgrep" || echo "✗ ripgrep"
which gh && echo "✓ gh" || echo "✗ gh"
which jq && echo "✓ jq" || echo "✗ jq"

echo "=== Tier 2 ==="
which arq && echo "✓ jena (arq)" || echo "✗ jena"
python3 -c "import yaml" 2>/dev/null && echo "✓ pyyaml" || echo "✗ pyyaml"

echo "=== Tier 3 ==="
obsidian help >/dev/null 2>&1 && echo "✓ obsidian CLI" || echo "✗ obsidian CLI (app may not be running)"

echo "=== Tier 4 ==="
which node && echo "✓ node" || echo "✗ node"
which npx && echo "✓ npx" || echo "✗ npx"
```
