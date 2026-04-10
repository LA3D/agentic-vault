---
type: implementation-note
repo: # [path-to-repo] — set your dev path during onboarding
language: []
status: active

# Edge fields (typed relationships — consumed by KG pipeline)
up: []             # Parent MOC or project
concept: []        # Concepts this implements
source: []         # Papers describing this implementation
related: []        # Related implementations

created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - "#status/active"

# Curator fields (uncomment if ontology fit is uncertain)
# curator_status: pending
# curator_suggested_type:
# curator_suggested_up:
# curator_observations:
#   - ""
---

# <% tp.file.title %>

**Repo**: `<% tp.file.cursor(1) %>`
**Status**: Prototype | Active | Archived
**Related**: [[Project Note]]

---

## What It Is

[Brief description]

---

## Architecture

[Key components, design decisions]

---

## Key Files

- `src/core/` -
- `experiments/` -

---

## Results & Learnings

[What worked, what didn't]

---

## Future Work

- [ ]
