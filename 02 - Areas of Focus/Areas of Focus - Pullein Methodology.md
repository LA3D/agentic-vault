---
type: reference
up: "[[VAULT-INDEX]]"
created: 2026-04-10
tags:
  - methodology
  - pullein
  - areas-of-focus
---

# Areas of Focus — Pullein Methodology

> Areas of focus are the foundation of your productivity system. Everything else — goals, projects, tasks — serves these areas. Based on Carl Pullein's GAPRA framework.

---

## What Are Areas of Focus?

Areas of focus are the 6-8 ongoing responsibilities and interests that define your life. Unlike projects (which have an end date), areas are perpetual — you maintain them, not complete them.

**Examples** (customize these for yourself during onboarding):
- **Research & Scholarship** — your intellectual work, publications, staying current
- **Health & Wellness** — physical health, mental health, routines
- **Self-Development & Learning** — skills, tools, courses, growth
- **Family & Relationships** — people you care about, community
- **Lifestyle & Experiences** — hobbies, travel, culture, quality of life
- **Finances** — financial health, planning, stability
- **Career & Professional** — job responsibilities, advancement, reputation
- **Life's Purpose** — overarching direction, values, meaning

---

## The GAPRA Hierarchy

```
Goals         ← Measurable outcomes with deadlines
  ↑ serve
Areas         ← THE FOUNDATION — ongoing life responsibilities (6-8)
  ↑ inform
Projects      ← Time-bound efforts (in 01 - Projects/)
  ↑ contain
Resources     ← Knowledge supporting the above (in 03 - Resources/)
  ↑ support
Actions/Tasks ← Individual to-dos within projects
```

Every project should connect to an area via the `area:` edge field. If a project doesn't serve any area, question why you're doing it.

---

## How to Use Areas in This Vault

### Area Notes (`02 - Areas of Focus/`)
Each area gets its own note created from `Templates/Area of Focus.md`. The area note defines:
- **What the area encompasses** and why it matters
- **Standards to maintain** — what "good enough" looks like
- **Current goals** — measurable, time-bound
- **Active projects** — what's serving this area right now
- **Recurring routines** — habits that maintain the standard

### Connecting Everything Back
- **Projects** use `area: "[[Area Name]]"` in frontmatter to declare which area they serve
- **MOCs** can also use `area:` to connect knowledge domains to areas
- The KG pipeline can query "what projects serve this area?" across the vault

### Review Cadences (Pullein)
- **Weekly quick-scan**: Am I doing *something* for each area? (5 minutes)
- **Six-month deep review**: Redefine standards, assess goals, simplify routines

---

## Setting Up Your Areas

Run `/onboarding` to create your areas interactively, or create them manually:

1. Choose 6-8 areas that cover your life responsibilities
2. Create a note for each in `02 - Areas of Focus/` using the Area of Focus template
3. Define standards and initial goals for each
4. Add the areas to VAULT-INDEX.md

**Pullein's key insight**: Plan no more than 50% of your time. Keep flexibility for the unexpected. Areas give you direction without rigidity.
