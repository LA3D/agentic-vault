---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - vault-reference
  - integrations
  - tools
---

# Integration Ecosystem

> This vault is a central processing hub — external tools feed information in, the vault structures and links it, and the knowledge graph makes it queryable. The specific tools are your choice; the pattern is what matters.

---

## The Ingestion Pattern

Every external source follows the same flow:

```
External Source  →  Triage/Processing  →  Encode into Vault  →  Wire into Graph
```

1. **External source** produces content (paper, highlight, email, web page, task)
2. **Triage** determines if it's worth encoding (most content is noise)
3. **Encode** creates a typed vault note via `/encode` (type, location, frontmatter, body)
4. **Wire** connects it to the knowledge graph (MOC listing, reciprocal links, edge fields)

The tools below plug into different points in this pipeline. You can start with zero integrations and add them as your needs grow.

---

## Tool Tiers

### Tier 0 — Essential (free, required)

| Tool | Purpose | Setup |
|------|---------|-------|
| **Git** | Version control for the vault | `brew install git` |
| **Claude Code** | The agent that operates the vault | Anthropic subscription |
| **Obsidian** | Markdown editor with graph view, plugins, templates | `brew install --cask obsidian` |

### Tier 1 — Knowledge Graph (free, recommended)

| Tool | Purpose | Setup |
|------|---------|-------|
| **Python 3 + PyYAML** | Frontmatter extraction for KG pipeline | `brew install python3 && pip install pyyaml` |
| **Apache Jena** | RDF conversion, SPARQL queries, SHACL validation | `brew install jena` |

With these installed, run `scripts/kg/build-graph.sh` to build the knowledge graph from your vault's frontmatter. This enables the `/vault-kg` skill for graph queries.

### Tier 2 — Enhanced Navigation (free, recommended)

| Tool | Purpose | Setup |
|------|---------|-------|
| **Obsidian CLI** | Fast indexed search (54x faster than grep) | Built into Obsidian 1.12+. Settings > General > CLI |

### Tier 3 — Google Workspace (free, recommended)

| Tool | Purpose | Setup |
|------|---------|-------|
| **GWS Skills** | Gmail, Calendar, Drive integration | Install GWS skill pack. Requires Google account + API setup with personal Gmail |

Setup involves creating a Google Cloud project, enabling APIs, and authenticating. The `gws-shared` skill walks through this.

### Tier 4 — Research Tools (free)

| Tool | Purpose | Skill |
|------|---------|-------|
| **arXiv / alphaxiv** | Paper discovery and summaries | `/alphaxiv-paper-lookup` |
| **Google NotebookLM** | AI-powered research synthesis | `/notebooklm` |
| **Zotero** | Reference management (open source) | Manual + Google Drive sync |
| **Quarto** | Document rendering (PDF, HTML, slides) | `/quarto` — `brew install --cask quarto` |

### Tier 5 — Premium Integrations (paid, optional)

These tools accelerate specific workflows. Free alternatives exist for each.

| Tool | Cost | What it adds | Free alternative |
|------|------|-------------|-----------------|
| **Readwise** | ~$8/mo | Automatic highlight sync from Kindle, web, podcasts, articles. Obsidian plugin creates structured highlight files. | Manual capture via `/encode`. Copy-paste highlights into concept notes. |
| **Todoist** | ~$4/mo | Task management with projects, labels, priorities. CLI (`td`) for agent-driven task ops. | Obsidian Tasks plugin (free, built into vault). Markdown checkboxes + query blocks. |
| **Paperpile** | ~$3/mo | Reference management with Google Docs integration, shared libraries. | Zotero (free, open source). Slightly different workflow but same purpose. |
| **Kindle Scribe** | Hardware | Handwritten notes + PDF annotation on e-ink. Export via email. | Any PDF annotation tool + manual import. |

---

## Integration Patterns by Workflow

### Reading Papers
```
Find paper (arXiv, Google Scholar, colleague recommendation)
  → Download PDF to reference manager (Zotero or Paperpile)
  → Store PDF in Google Drive or local folder
  → Create literature note: /encode with type: literature-note
  → Link to concepts, add to LITERATURE-INDEX
```

### Processing Highlights (with Readwise)
```
Read on Kindle/web/podcast app
  → Highlights sync to Readwise → Obsidian plugin creates files
  → Triage: /process-readwise skill identifies signal
  → Promote to vault notes via /encode
```

### Processing Highlights (without Readwise)
```
Read anywhere → manually copy key quotes/insights
  → Create vault note: /encode or /obsidian-knowledge-capture
  → Attribute source, add edge fields
```

### Task Management (with Todoist)
```
Capture tasks in Todoist (voice, app, email forward)
  → Use td CLI or /todoist skill to review
  → Link tasks to vault projects
```

### Task Management (without Todoist)
```
Use markdown checkboxes in project notes and daily notes
  → Obsidian Tasks plugin for query blocks
  → /audit checks for orphaned tasks
```

### Web Content
```
Find interesting article/blog post
  → Use defuddle CLI or WebFetch to extract content
  → Create external-resource note via /encode
  → Link to relevant concepts and MOCs
```

---

## Configuring During Onboarding

The `/onboarding` skill asks what tools you use and configures accordingly:

- **Reference manager**: Zotero / Paperpile / none → sets up linking-guide conventions
- **Highlight capture**: Readwise / manual → installs skill if applicable
- **Task management**: Todoist / Obsidian Tasks → configures task-management rule
- **Document rendering**: Quarto / Pandoc / none

You can change these later — the vault works at any integration level.
