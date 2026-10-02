---
name: encode
description: Create, update, or wire typed notes in this Obsidian vault when the user asks to save or integrate knowledge. Handles source capture, routing, conceptual links, and verification. Read-only questions use retrieve; explicit note reviews use review-note.
---

# Encode

Turn requested knowledge into useful, retrievable vault memory. Use the saved
vault and established user scope. Reading a source or discovering an action item
alone does not authorize saving it or creating an external task.

## Scope

Accept natural language or caller fields: `content_description`, `suggested_type`,
`suggested_title`, `source_material`, `creation_context`, `extra_frontmatter`,
`skip_commit`. Return affected paths, routing, connections, review outcome, and
material limits.

- **Bounded update:** read the known note and relevant evidence; preserve its
  structure and unrelated metadata. Check changed facts and links inline.
- **Source capture or substantive synthesis:** read and apply
  [capture-quality.md](references/capture-quality.md). Raw preservation and
  integration are distinct outcomes; complete the one requested.
- **Explicit raw-only preservation:** preserve the original body and provenance,
  add the requested locator/index entry, and identify it as an archive. Do not
  expand into synthesis or imply conceptual integration was completed.
- **Wire:** discover justified connections, update the relevant index and
  reciprocals, and verify changed files without unnecessary content rewriting.
- **Fleeting thought:** use `05 - Watching/`, `type: fleeting-note`, `created:`,
  `status: watching`, tags, and `area:` if known. No MOC entry or maturity required.

## Find and route

Search existing coverage before creating. Use filesystem reads/search; apply
`.claude/skills/retrieve/SKILL.md` for multi-note evidence. Read known single notes
directly. Keep paths distinct when titles are ambiguous. Update existing coverage
when it meets the request. Ask only when consequential ambiguity remains after
using the user's instructions and available evidence.

For new notes, read [router.md](agents/router.md), relevant routing corrections in
`.claude/agent-memory/encode-router/MEMORY.md`, and applicable entries in
`.claude/rules/typed-relationships.md` and
`03 - Resources/Obsidian Reference/Vault Vocabulary.md`. Apply routing inline
when clear; a router agent is optional. Empty template fields are not all required.

## Write and integrate

Apply this section to maintained notes. Explicit raw-only preservation and
fleeting thoughts retain the narrower metadata and integration scope above.

Apply the relevant template, replacing placeholders and omitting irrelevant
sections. Set canonical `type:`, `created:`, actual `created_by:` identity (Claude
in this harness), `creation_context:`, and useful tags. Preserve prior authorship
on updates. Apply `maturity: draft` only to types covered by the maturity rules.
Follow CLAUDE.md Git attribution policy rather than template agent names.

Populate applicable edges with verified targets. Projects and MOCs have `area:`;
other area relationships may be inherited through `up:` where allowed. Prefer
claim-form concept titles when appropriate. Attribute claims and distinguish
interpretation from evidence. Consult the style guide for substantial prose,
not every metadata change.

For published sources, apply [published-author identity](references/capture-quality.md#published-author-identity)
to resolve reusable author notes and authorship edges before completing integration.

List new maintained notes in the relevant MOC/sub-index: literature in
LITERATURE-INDEX, external sources in the relevant external index, tools in
TOOLS-INDEX. Change VAULT-INDEX only for major entry points. Respect bounded
branching in touched sections without unrelated index reorganization.

Conceptual discovery is part of source-capture completion. Read candidate
concepts and relevant neighbors through filesystem links or a fresh KG; follow
useful second-hop connections to resolve coverage or tensions. No full rebuild
is required for discovery. Apply the shared contract to missing relationships,
not only already-populated edges.

Add justified reciprocal body links on concept targets and symmetric `related:`
links. Assert `supports:`, `criticizes:`, or `extends:` only when source-grounded
and within scope. A body back-reference does not authorize rewriting a neighbor's
substantive claims. Report uncertain relationships instead of asserting them.
Do not author KG-generated inverses. Citations need no automatic reciprocal edit.

## Verify and review

Read saved changes and inspect the scoped diff:

- YAML parses; applicable required metadata exists; no template placeholders remain.
  Preserve explicit fleeting/raw-only exceptions.
- Added/changed links resolve to intended paths and satisfy vocabulary domain/range.
  A limited search is not proof of absence.
- Required indexing and justified conceptual integration are complete.
- Changed claims match evidence, including qualifications; source-backed maintained
  notes pass [capture-quality.md](references/capture-quality.md).
- Edits stay within the requested outcome. Unrelated existing debt is not a
  prerequisite repair.

Apply the relevant `.claude/skills/review-note/SKILL.md` criteria inline for routine
creation or updates, and use independent review for substantive capture, synthesis,
and conceptual rewrites. For explicit reviews follow the requested scope. One independent reviewer suffices for
substantive capture: give it the source, saved changes, scope, and shared criteria,
not the desired verdict. Bounded updates/raw-only preservation use focused inline
checks unless complexity warrants review. Fix confirmed failures and recheck
before committing. If independent review cannot run, report the limitation;
do not claim it passed.

## Finish

Follow `.claude/rules/discipline-gates.md` and CLAUDE.md Git policy. Stage specific
reviewed files and commit one coherent batch unless `skip_commit: true` or the
user says otherwise. The batch caller owns the commit. Do not push without
authorization. After graph-affecting changes, launch one background rebuild with
`scripts/kg/rebuild-async.sh` when available; distinguish launch from success.
Unrelated graph errors do not invalidate a verified local change or authorize
broader remediation.

Report the saved knowledge, meaningful connections, review result, commit state,
and material limits. Link counts and elaborate wiring reports are optional;
neither substitutes for semantic coverage.
