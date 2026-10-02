---
name: vault-curator
description: "Analyze vault structure, propose concrete restructuring, review ontology suggestions and evolve the vault's type taxonomy. Use for reviewing curator observations on notes, promoting vocabulary changes, and ontology governance. For structural health checks (orphans, dangling refs, type validity), use /audit instead."
disable-model-invocation: false
---

# Vault Curator

Maintain and evolve the vault's ontology — its type system, edge fields, MOC hierarchy, and domain/range constraints.

## Activation

- `/curator` — Full run: audit → analyze → review → evolve (calls `/audit` first for health baseline)
- `/curator review` — Harvest and process pending suggestions
- `/curator evolve` — Turn accepted proposals into concrete changes
- `/curator analyze` — Inspect topology and navigation; propose concrete restructuring

> **Note**: `/curator health` has been replaced by `/audit`. Use `/audit` for structural health checks (orphans, dangling refs, type validity, discoverability). Curator focuses on ontology governance.

---

## Key Files

| File | Role |
|------|------|
| `03 - Resources/Obsidian Reference/Vault Vocabulary.md` | Canonical vocabulary (validate against this) |
| `03 - Resources/Obsidian Reference/Vault Type Taxonomy.md` | Browsable reference |
| `.claude/rules/typed-relationships.md` | Claude Code enforcement rules |
| `03 - Resources/Obsidian Reference/Ontology-Evolution-Log.md` | Provenance record |

---

## Health Checks → Use `/audit`

Structural health checks (type validity, orphans, dangling refs, template drift, discoverability) have moved to the `/audit` skill. Use `/audit` for standalone health checks or `/audit session` for session-scoped checks.

When running the full curator (`/curator`), Audit runs first to establish the health baseline.

---

## Mode 2: Review Suggestions (`/curator review`)

Harvest and process pending ontology observations.

### Step 1: Find pending suggestions

```bash
grep -rn "^curator_status: pending" --include="*.md" .
```

### Step 2: Read each flagged note

For each note with `curator_status: pending`, read:
- `curator_suggested_type:` — proposed reclassification
- `curator_suggested_up:` — proposed hierarchy change
- `curator_observations:` — reasoning

### Step 3: Group by observation type

Categorize suggestions:
- **Reclassification**: Note type should change
- **New edge needed**: Relationship doesn't map to existing fields
- **New MOC needed**: Cluster of notes without a parent scheme
- **Scope drift**: Note has outgrown its type
- **New vocabulary**: Proposed new type or literatureType value

### Step 4: Present grouped summary

Show the user a summary table per category with note links and observation text.

### Step 5: Process decisions

For each group, ask the user: accept / decline / defer.

- **Accept**: Set `curator_status: accepted`; put vocabulary proposals in "Proposed Extensions" in Vault Vocabulary, and navigation/capture proposals in a concrete plan or scoped Encode queue
- **Decline**: Set `curator_status: declined`
- **Defer**: Leave as `curator_status: pending`

### Step 6: Commit

```bash
git add [modified notes] "03 - Resources/Obsidian Reference/Vault Vocabulary.md"
git commit -m "[Agent: Claude] curator: review N suggestions (A accepted, D declined)"
```

---

## Mode 3: Evolve Ontology (`/curator evolve`)

Turn accepted proposals into concrete vocabulary changes.

### Step 1: Read proposals

Read approved session plans and scoped Encode queues as well as the "Proposed Extensions" section of `03 - Resources/Obsidian Reference/Vault Vocabulary.md`. Navigation and concept-capture changes do not require a vocabulary amendment.

### Step 2: Generate plan for each proposal

For each accepted proposal, determine:
- What changes in Vault Vocabulary (new type row, new edge row, scope change)
- What changes in `typed-relationships.md`
- What changes in `Vault Type Taxonomy.md`
- Whether templates need updating
- How many existing notes are affected
- Whether a new MOC needs creating

### Step 3: Present plan to user

Show the full change plan with file list and note counts. Obtain approval for new decisions; reuse explicit approval already given for this plan.

### Step 4: Execute approved changes

On approval:

1. **Update Vault Vocabulary**: Move proposal from "Proposed Extensions" to the canonical tables
2. **Update typed-relationships.md**: Add new types/fields to the rules
3. **Update Vault Type Taxonomy.md**: Add new entries to the browsable reference
4. **Update templates**: Add new fields if applicable
5. **Batch-update notes**: Reclassify, add new edge fields, update `up:` as needed
6. **Clear resolved curator fields**: Remove only implemented observations and suggestions. Retain unresolved observations and their accepted/pending status; clear the status only when none remain.

### Step 5: Log the evolution

Add entry to `03 - Resources/Obsidian Reference/Ontology-Evolution-Log.md`:
- Date, type of change, actor, trigger
- What changed and why
- Notes affected

### Step 6: Commit

```bash
git add [all modified files]
git commit -m "[Agent: Claude] curator: evolve vocabulary — [brief description]

- [list changes]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Full Curator (`/curator`)

Run audit → analyze → review → evolve. Audit establishes the health baseline;
analyze reads structural candidates and produces concrete proposals; review
collects decisions on both those proposals and pending observations; evolve
executes only approved changes. Analysis and evidence gathering are read-only and
need no separate approval. Existing session authorization carries forward.
Do not require another confirmation for an already approved proposal. End with
applied changes, review/validation results, and remaining concrete decisions.

---

## Structural analysis (`/curator analyze`)

Analyze the organization before deciding what to change. Start with a completed
fresh graph build (`bash scripts/kg/rebuild-async.sh`); inspect its exit status
and report, rather than assuming a launched or lock-skipped build succeeded.
If graph tooling is unavailable, continue filesystem section counts and candidate
reading, identify the limitation, and do not present stale topology as current.

1. Run `hub-notes.rq` from `scripts/kg/sparql/` to select candidates. Incoming
   degree identifies attention points; it is not a direct-child routing count.
2. Resolve each selected anchor URI from the graph, retaining its vault-relative
   path when titles collide. Substitute that URI for `NOTE_URI` in
   `cold-neighbors.rq` and `cross-moc-bridges.rq`. Read candidate bodies and their
   parents; low degree alone does not establish missing integration.
3. Group concept references by their `up:` parents. Inspect repeated concepts,
   dangling targets, and same-title notes using filesystem evidence as well as
   typed edges. Markdown headings and body navigation are not fully represented
   in the graph: count direct entries in the actual index/MOC sections.
4. For touched navigation nodes exceeding 12 direct choices, propose bounded
   subsections or sub-indexes. Count links at their own level; preserve nested
   entries with their parent. Do not split a coherent concept solely by degree.

### Concrete proposals and handoff

A full run must end with actionable proposals, or state that the checked scope
needs none. Do not stop at a topology narrative. For each supported proposal give:

- Evidence and affected vault-relative paths; distinguish count findings from
  semantic judgments based on reading.
- An exact before/after entry-to-section mapping for navigation restructuring,
  with per-section counts, no duplicated/lost entries, and preserved descriptions.
- For concept consolidation: existing coverage, source paths, proposed title and
  outline, justified neighbors, distinctions/limitations to retain, and the
  Encode + Review Note handoff. Preserve original source bodies.
- For ambiguous titles: separate scopes, chosen canonical paths/titles, and each
  referring file's intended destination. Preserve distinct knowledge bodies.
- Validation plan and queue/log updates, including what remains unresolved.

Read-only analysis does not authorize edits. Reuse decisions already authorized
in the session; ask only for genuinely new decisions. Once approved, carry out
bounded navigation/link edits, route substantive captures through Encode and
independent Review Note, log the changes, and rebuild once after the final batch.
Clear only resolved curator observations; retain remaining accepted proposals.
Do not expand restructuring into unrelated repository or graph remediation.

---

## Principles

- **Never auto-modify the ontology**. Always present proposals and wait for approval.
- **Violations are warnings, not errors**. The domain/range table describes expected patterns, not hard constraints.
- **Keep scope bounded**. Repair only approved fields and relationships; unrelated legacy cleanup requires separate scope.
- **Provenance matters**. Every vocabulary change gets logged in the Evolution Log.
- **Markdown is authoritative**. The generated RDF graph supplements filesystem reading; edit maintained YAML and Markdown, not generated graph files.

---

## Integration with Other Skills

Note-creation skills (`encode`, `obsidian-knowledge-capture`, and any batch ingest skills) populate curator fields when they observe ontology fit issues. The curator harvests these observations in `/curator review`.

See `.claude/rules/typed-relationships.md` → "Curator Observation Fields" for the field specification and population triggers.
