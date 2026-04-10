---
type: literature-note
literatureType: research-paper
authors:
author: []              # Wikilink to author note (graph edge)
year: <% tp.date.now("YYYY") %>
venue:
citekey:
topics: []
status: unread

# Edge fields (typed relationships — consumed by KG pipeline)
up: []             # Parent MOC or topic group
concept: []        # Main concepts introduced/discussed
criticizes: []     # Papers/concepts this critiques
supports: []       # Papers/concepts this supports
source: []         # Papers this cites/builds on
related: []        # Related papers (lateral)

zotero:
pdf:
created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - "#status/unread"

# Curator fields (uncomment if ontology fit is uncertain)
# curator_status: pending
# curator_suggested_type:
# curator_suggested_up:
# curator_observations:
#   - ""
---

# <% tp.file.title %>

## Summary

[One paragraph in your own words]

## Key Contributions

-

## Methodology

[How they did it]

## Results

[What they found]

## Related Concepts

- [[Concept 1]] — how it connects

## Connections

[Links to related vault notes — concepts, other literature, projects]

## Critical Analysis

[Strengths, limitations, questions]

## Annotations

[Extract from Zotero or manual notes]
