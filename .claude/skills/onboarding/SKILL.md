---
name: onboarding
description: "First-time vault setup: interview the user, populate owner-context.md, create areas of focus, configure KG namespace, set dev environment path. Use when the vault is fresh (owner-context.md is empty) or when the user says 'onboarding', 'setup', 'configure vault', or 'get started'. Also trigger proactively on first session if owner-context.md has no Name field populated."
---

# Onboarding

Walk a new user through vault setup via a structured interview. Populates configuration files, creates area notes, and configures the knowledge graph pipeline.

---

## When to Trigger

- First session in a fresh vault (owner-context.md is blank)
- User says "onboarding", "setup", "configure", "get started"
- Proactively if owner-context.md has no `**Name**:` value filled in

---

## Step 0: Environment Check

Before the interview, silently check what tools are installed. Report a summary to the user:

```bash
# Run these checks and build a report
echo "=== Environment Check ==="
which git >/dev/null 2>&1 && echo "✓ git" || echo "✗ git (required)"
which rg >/dev/null 2>&1 && echo "✓ ripgrep" || echo "✗ ripgrep (strongly recommended — brew install ripgrep)"
which gh >/dev/null 2>&1 && echo "✓ gh" || echo "✗ gh (recommended — brew install gh)"
which jq >/dev/null 2>&1 && echo "✓ jq" || echo "✗ jq (recommended — brew install jq)"
which arq >/dev/null 2>&1 && echo "✓ jena/arq" || echo "✗ jena (needed for KG — brew install jena)"
python3 -c "import yaml" 2>/dev/null && echo "✓ pyyaml" || echo "✗ pyyaml (needed for KG — pip install pyyaml)"
which node >/dev/null 2>&1 && echo "✓ node" || echo "✗ node (needed for skill marketplace — brew install node)"
which npx >/dev/null 2>&1 && echo "✓ npx" || echo "✗ npx (comes with node)"
obsidian help >/dev/null 2>&1 && echo "✓ obsidian CLI" || echo "○ obsidian CLI (enable in Obsidian Settings → General → CLI)"
```

Present the results and offer to help install missing tools:

> "Here's what I found on your system. The vault works with just git + Claude Code, but more tools unlock more capabilities. See `SETUP.md` for the full tier guide."

**If critical tools are missing** (git), stop and help install them before proceeding.
**If recommended tools are missing** (ripgrep, jena, node), note them but continue — the user can install later.

---

## Interview Sequence

Run these steps in order. Each step is a conversation turn — ask, wait for response, then proceed.

### Step 1: Who Are You?

Ask the user about themselves. Frame it as personalization, not data collection:

> "I'd like to learn about you so I can tailor how I work with you. This goes into `.claude/rules/owner-context.md` — I read it every session to remember your context. You can edit it anytime."

**Questions** (adapt conversationally, don't fire all at once):
- What's your name? What should I call you?
- What do you do? (role, institution/company, field)
- What are you working on right now? (active projects, research areas)
- What tools and languages do you use?
- How do you prefer to interact? (concise vs. detailed, push back vs. defer, etc.)
- What domains are you expert in? (so I don't over-explain)

**Action**: Populate `.claude/rules/owner-context.md` with their responses, following the section structure in the template.

### Step 2: What Are Your Areas of Focus?

Explain the Pullein/GAPRA framework briefly:

> "This vault organizes everything around Areas of Focus — the 6-8 ongoing responsibilities that define your life. Unlike projects (which end), areas are perpetual. Everything else connects back to an area."

**Show the defaults** from `[[Areas of Focus - Pullein Methodology]]`:
- Research & Scholarship
- Health & Wellness
- Self-Development & Learning
- Family & Relationships
- Lifestyle & Experiences
- Finances
- Career & Professional
- Life's Purpose

**Ask**: "These are starting suggestions. Which resonate? Want to rename, add, or remove any?"

**Action**: For each confirmed area, create a note in `02 - Areas of Focus/` using `Templates/Area of Focus.md`. Then update VAULT-INDEX.md with the area list.

### Step 3: Knowledge Graph Namespace

Explain what this is and why it matters:

> "The vault builds a knowledge graph from your note relationships. The graph needs a namespace — a base URL for identifying notes as RDF resources. If you own a domain, you can use it (e.g., `https://yourdomain.com/vault/`). Otherwise, the default `https://example.com/vault/` works fine and can be changed later."

**Ask**: "Do you have a preferred domain, or should we keep the default?"

**Action**: If they provide a custom namespace, run:
```bash
scripts/kg/setup-namespace.sh <their-namespace>
```

If they keep the default, do nothing — files already use `https://example.com/vault/`.

### Step 4: Development Environment

Ask about their coding setup:

> "If you write code, I can link your vault notes to your repositories. Where do your git repos live?"

**Questions**:
- Where are your code repos? (e.g., `~/dev/git/`, `~/projects/`, `~/code/`)
- What GitHub organizations do you work with?

**Action**:
- Update the "Development Environment" section of owner-context.md
- Update the `repo:` default in `Templates/Implementation Note.md` if they have a standard path

### Step 5: Tool Inventory

Ask what external tools they use (don't push paid tools):

> "The vault can integrate with various tools for processing research, managing tasks, and capturing highlights. What do you currently use?"

**Categories** (reference `[[Integration Ecosystem]]` for details):

| Category | Options |
|----------|---------|
| Reference management | Zotero / Paperpile / none |
| Highlight capture | Readwise / manual / none |
| Task management | Todoist / Obsidian Tasks / none |
| Google Workspace | Gmail/Calendar/Drive — personal account? |
| Document rendering | Quarto / none |

**Action**: Note their tool choices in owner-context.md. If they have tools that need skills installed, point them to the Integration Ecosystem doc and relevant skill installation.

### Step 6: Verification and Next Steps

Read back a summary of what was configured:

```
## Setup Summary

**Owner**: [Name] — [Role] at [Institution]
**Areas**: [list]
**KG Namespace**: [namespace]
**Dev Path**: [path]
**Tools**: [list]

### Files Created/Modified:
- .claude/rules/owner-context.md (populated)
- 02 - Areas of Focus/[Area].md (N area notes)
- VAULT-INDEX.md (updated with areas)
- scripts/kg/ (namespace configured, if custom)
```

**Suggest first actions**:
- "Try creating your first project: tell me about something you're working on and I'll use `/encode` to set it up"
- "If you have papers to track, we can start building your literature notes"
- "Run `/research-session` when you're ready for a structured deep dive on a topic"

---

## Discipline Gates

- **Do NOT skip the interview** — the vault works much better when owner-context.md is populated
- **Do NOT create areas the user didn't confirm** — present defaults but let them choose
- **Do NOT run setup-namespace.sh unless the user provided a custom namespace** — the default is fine
- **Read back the summary** before committing — verification gate applies

---

## Commit

After all steps:

```bash
git add .claude/rules/owner-context.md "02 - Areas of Focus/" VAULT-INDEX.md Templates/
git commit -m "$(cat <<'EOF'
[Agent: Claude] Onboarding: configure vault for [user name]

- Populated owner-context.md
- Created N area of focus notes
- Configured KG namespace: [namespace]
- Updated VAULT-INDEX with areas

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```
