---
name: review-note
description: Review vault notes for structural validity, source fidelity, conceptual integration, and recoverability. Use for requested note review or Encode's creation quality check, including batches. Use audit for vault-wide structural health checks.
---

# Review Note

Review the requested note or batch against source evidence and maintained vault standards. Keep findings and repairs within the user's scope. Read-only review produces findings; it does not change notes, links, or maturity.

**Usage:** `/review-note path/to/note.md` or a folder for an explicitly requested batch. `--draft` reports clear substantive problems and skips stylistic polish. `--final` performs full applicable checks and may report improvements. Default to `--final`; this selects coverage, not permission to edit or promote.

## Scope and execution

- Routine bounded edits can be reviewed inline against changed facts, fields, and links, without separate agents.
- Substantive source captures and synthesis require an independent reviewer, separate from the authoring pass. One reviewer is sufficient; provide the source, proposed notes, relevant standards, and retrieval access without prescribing expected findings. Add specialists only when the task warrants them.
- Check structure first. Resolve structural blockers that prevent interpreting the note before dependent content/integration checks. Within an authorized editing task, repair and recheck; in a read-only task, report blockers and identify checks still possible or deferred.
- Review content and integration after relevant structure is understood. Consolidate only after reviewers' findings arrive. The author can consolidate inline, dismissing unsupported findings with reasons.
- Batch mode retains requested depth and does not waive independent review for substantive captures. One independent pass can cover a coherent batch.
- Draft and batch captures still require source fidelity, recoverability, and conceptual integration. A draft permits uncertainty and unfinished prose, not silently omitted integration. Explicit raw-preservation requests are assessed against their narrower scope.

If independent review is unavailable, complete remaining checks and report the limitation; do not describe self-review as independent or mark a substantive capture fully reviewed.

## Required references

Read relevant current standards rather than copying field/domain tables:

- `03 - Resources/Obsidian Reference/Vault Vocabulary.md`: canonical types and edge domains/ranges.
- `.claude/rules/typed-relationships.md`: required metadata, maturity, and deprecated fields.
- [Capture quality](../encode/references/capture-quality.md): required for substantive source capture and synthesis; shared recoverability and conceptual-discovery contract.
- Original source or preserved source Markdown, relevant existing notes, and target MOC/index: content and integration evidence.

Use filesystem retrieval with vault-relative paths as identities; follow the available Retrieve skill for multi-note discovery. Read candidate notes before proposing conceptual links. Existing edges do not exhaust relevant concepts: a research capture with no `concept:` field still needs conceptual discovery.

## Checks

**Structure:** Verify canonical type and semantic fit, metadata required for that type, typed-edge domains/ranges, dates, and deprecated fields. Resolve link targets by path where titles collide. Use the vocabulary's actual `source:` range, including external-resource targets where permitted.

**Content:** Verify bibliographic identity (source title, authors, publication date/year, and URL or citekey where applicable) against the source, not template defaults. Compare maintained notes with sources for attribution, exact relevant particulars, qualifications, and uncertainty. Apply the shared capture contract, including recoverability without the source or binary attachments. Check relevant neighboring claims for material contradictions; distinguish explicit scholarly disagreement from accidental conflation. State unavailable evidence and its effect on confidence.

**Integration:** Check parent/index placement, applicable reciprocal navigation and relevant neighborhood discovery, resolving links, existing coverage, and project area relationships. For substantive research capture, independently discover relevant concepts and verify justified typed relationships even when none were submitted. Index-only placement does not establish conceptual integration. Recommend new notes only when existing coverage cannot support requested work; use Encode for authorized creation.

**Author resolution:** For published captures, check the shared [published-author identity](../encode/references/capture-quality.md#published-author-identity) rule: verified bylines/aliases, canonical authorship targets, selective new author-note justification, and reciprocal works navigation. Report reused/created identities or unresolved ambiguity; do not treat author-note coverage as personal-contact management.

**Style:** When requested or useful in final review, consult `03 - Resources/context/ai_ese.md` and `fastai_style_guide.md` in that directory. Flag material clarity problems; stylistic preferences do not block capture and numerical scores are not required.

## Findings and repairs

Report note paths, scope, checks performed, and limitations. Rank supported findings:

- **Error:** factual inaccuracy, invalid structure or links, missing required metadata, or failure of applicable capture-quality requirements.
- **Warning:** supported weakness that does not violate requested completion criteria.
- **Suggestion:** optional improvement outside required completion.

Include evidence and a concrete repair for substantive findings. Mark uncertainty; do not invent findings to fill categories. When repairs are authorized, recheck affected criteria. Stop once relevant checks pass; report unrelated issues without expanding the task.

## Maturity

Successful final review is necessary for promotion but does not itself authorize mutation. Promote only within an authorized editing/finalization task or explicit promotion request, after all applicable checks complete with no unresolved Errors. Draft review, unavailable required independent review, or unverified required source checks cannot support promotion.

For eligible knowledge-note types, follow `.claude/rules/typed-relationships.md`: `draft` (or absent maturity) may become `validated`; retain existing `validated` or `core`. Do not change taxonomy or promote structural/organizational notes. Read-only review reports eligibility without changing frontmatter.
