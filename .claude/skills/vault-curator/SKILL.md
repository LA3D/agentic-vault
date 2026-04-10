---
name: vault-curator
description: "Review ontology suggestions and evolve the vault's type taxonomy. Use for reviewing curator observations on notes, promoting vocabulary changes, and ontology governance. For structural health checks (orphans, dangling refs, type validity), use /audit instead."
disable-model-invocation: false
---

# Vault Curator

Maintain and evolve the vault's ontology — its type system, edge fields, MOC hierarchy, and domain/range constraints.

## Activation

- `/curator` — Full run: audit → review → evolve (calls `/audit` first for health baseline)
- `/curator review` — Harvest and process pending suggestions
- `/curator evolve` — Turn accepted proposals into concrete changes

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

- **Accept**: Set `curator_status: accepted`, write proposal to "Proposed Extensions" in Vault Vocabulary
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

Read the "Proposed Extensions" section of `03 - Resources/Obsidian Reference/Vault Vocabulary.md`.

### Step 2: Generate plan for each proposal

For each accepted proposal, determine:
- What changes in Vault Vocabulary (new type row, new edge row, scope change)
- What changes in `typed-relationships.md`
- What changes in `Vault Type Taxonomy.md`
- Whether templates need updating
- How many existing notes are affected
- Whether a new MOC needs creating

### Step 3: Present plan to user

Show the full change plan with file list and note counts. Wait for approval.

### Step 4: Execute approved changes

On approval:

1. **Update Vault Vocabulary**: Move proposal from "Proposed Extensions" to the canonical tables
2. **Update typed-relationships.md**: Add new types/fields to the rules
3. **Update Vault Type Taxonomy.md**: Add new entries to the browsable reference
4. **Update templates**: Add new fields if applicable
5. **Batch-update notes**: Reclassify, add new edge fields, update `up:` as needed
6. **Clear curator fields**: Remove `curator_status`, `curator_suggested_*`, `curator_observations` from processed notes

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

## Mode 3: Full Curator (`/curator`)

Run in sequence:

1. **Audit** → call `/audit` for structural health baseline
2. **Review** → process pending suggestions (Mode 1 above)
3. **Evolve** → implement accepted proposals (Mode 2 above)

Present the audit report first. If there are pending suggestions, proceed to review. If there are accepted proposals, proceed to evolve. At each stage, wait for user input before continuing.

---

## Principles

- **Never auto-modify the ontology**. Always present proposals and wait for approval.
- **Violations are warnings, not errors**. The domain/range table describes expected patterns, not hard constraints.
- **Fix on contact**. When the curator touches a note for suggestion processing, opportunistically fix legacy fields (noteType → type, remove relatedConcepts, etc.).
- **Provenance matters**. Every vocabulary change gets logged in the Evolution Log.
- **Obsidian-native**. No RDF serialization, no external tooling. YAML frontmatter, markdown files, and Claude Code rules.

---

## Integration with Other Skills

Note-creation skills (`encode`, `obsidian-knowledge-capture`, and any batch ingest skills) populate curator fields when they observe ontology fit issues. The curator harvests these observations in `/curator review`.

See `.claude/rules/typed-relationships.md` → "Curator Observation Fields" for the field specification and population triggers.
