---
name: audit
description: "Structural health check for the vault's knowledge graph. Two modes: standalone (/audit) runs a full vault health check with type validity, orphans, dangling refs, discoverability, and cold areas. Session-scoped (/audit session) checks only notes changed this session. Produces severity-ranked reports. Use when: 'audit', 'vault health', 'health check', 'structural check', 'what's broken', or at session end for quality review. Flags issues but does NOT fix them — that's the user's decision."
---

# Audit

Structural health check for the vault. Consolidates checks previously split across vault-curator and vault-kg into one authoritative report. Two modes: standalone (full vault) and session-scoped (git diff).

**Audit flags, it doesn't fix.** The report is advisory — the user decides what to act on.

---

## Mode Detection

| Signal | Mode |
|--------|------|
| `/audit`, "vault health", "health check", "what's broken" | **Standalone** (full vault) |
| `/audit session`, "check what we created", at session end | **Session** (git diff scoped) |

---

## Standalone Mode (`/audit`)

Full vault health check. Run all checks, produce a severity-ranked report.

### Step 0: Graph Freshness

Same as Retrieve — verify `scripts/kg/vault-graph-full.ttl` is current. If stale, rebuild:
```bash
scripts/kg/rebuild-async.sh
```
Wait for completion before running SPARQL checks (~6s).

### Check 0: SHACL Validation (W3C formal constraints)

Run SHACL validation against the full graph. This is the formal, machine-checkable layer — it complements the SPARQL checks below.

**If `validation-summary.txt` exists and is recent** (< 10 minutes old), read it instead of re-running validation:

```bash
# Check if summary exists and is fresh
SUMMARY="scripts/kg/validation-summary.txt"
if [[ -f "$SUMMARY" ]] && [[ $(( $(date +%s) - $(stat -f %m "$SUMMARY") )) -lt 600 ]]; then
    cat "$SUMMARY"
else
    # Run validation directly
    cd scripts/kg && shacl validate --shapes=vault-shapes.ttl --data=vault-graph-full.ttl > validation-report.ttl 2>&1
    # Generate summary
    grep "sh:resultMessage" validation-report.ttl \
        | sed 's/.*sh:resultMessage *"//' | sed 's/".*//' \
        | sort | uniq -c | sort -rn
fi
```

The summary is also written automatically by `rebuild-async.sh` after every `/encode` commit. So in practice, this check often just reads a pre-computed report.

**Severity mapping**: SHACL `sh:Violation` → **Error**. SHACL `sh:Warning` → **Warning**. SHACL `sh:Info` → **Info**.

**What SHACL catches that SPARQL checks don't**:
- Formal shape conformance (every Project must have `area:`, every MOC must have `up:`)
- Dangling references (edges pointing to URIs with no type in the graph)
- Cross-node constraints via embedded SPARQL

**What SPARQL checks catch that SHACL doesn't**:
- Type validity against the evolving canonical list (SHACL shapes are static)
- Template drift (expected fields per type)
- Discoverability distribution (bucket analysis)
- Freshness (git-based staleness detection)

The two layers are complementary — SHACL is the formal contract, SPARQL checks are the operational monitoring.

### Check A: Type Integrity

**A1. Type Validity** — Compare all types in the graph against the canonical 22 types:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
SELECT ?type (COUNT(?note) AS ?count) WHERE {
    ?note a ?type .
} GROUP BY ?type ORDER BY DESC(?count)
SPARQL
)
```

Compare returned types against the canonical type list in `03 - Resources/Obsidian Reference/Vault Vocabulary.md` (the authoritative source — don't hard-code the list here, as it evolves via `/vault-curator evolve`). Non-canonical types → **Error**.

**A2. Template Drift** — Notes missing expected fields for their type. Use Glob + Read (not grep — filenames have spaces):

```bash
# For literature notes, check a sample for missing fields:
# Glob for "03 - Resources/Literature/@*.md", Read frontmatter of first 10,
# check for authors:, year:, title: fields
```

Expected fields by type:

| Type | Required | Expected |
|------|----------|----------|
| `literature-note` | `type`, `up` | `authors`, `year`, `title` |
| `concept-note` | `type`, `up` | `status` |
| `project` | `type` | `area`, `status` |
| `author-note` | `type`, `up` | `aliases` |
| `external-resource` | `type`, `up` | `url` |
| `tool` | `type`, `up` | — |

Missing required fields → **Error**. Missing expected fields → **Warning**.

### Check B: Structural Integrity

**B1. Hierarchy (`up:` Population)** — Notes missing their place in the hierarchy:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?title ?type WHERE {
    ?note a ?type .
    ?note dcterms:title ?title .
    FILTER(?type NOT IN (vault:Area, vault:daily, vault:FleetingNote))
    FILTER NOT EXISTS { ?note vault:up ?parent }
    FILTER(!CONTAINS(STR(?note), "Readwise"))
    FILTER(!CONTAINS(STR(?note), "Inbox"))
} ORDER BY ?type ?title
SPARQL
)
```

Notes missing `up:` (excluding areas, daily, fleeting, Readwise) → **Warning**.

**B2. Domain/Range Violations** — Edge fields pointing to wrong type targets. Sample check for `concept:`:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?sourceTitle ?sourceType ?targetTitle ?targetType WHERE {
    ?source vault:concept ?target .
    ?source a ?sourceType .
    ?source dcterms:title ?sourceTitle .
    ?target a ?targetType .
    ?target dcterms:title ?targetTitle .
    FILTER(?targetType NOT IN (vault:ConceptNote, vault:TheoryNote, vault:MethodNote))
} LIMIT 20
SPARQL
)
```

Repeat for `source:` (targets should be LiteratureNote/BookNote), `extends:` (targets should be TheoryNote/ConceptNote/MethodNote). Violations → **Warning**.

### Check C: Connectivity

**C1. Orphan Detection** — Notes with no incoming edges:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?type (COUNT(?note) AS ?orphans) WHERE {
    ?note a ?type .
    ?note dcterms:title ?title .
    FILTER NOT EXISTS {
        ?other ?pred ?note .
        FILTER(?pred NOT IN (rdf:type, dcterms:title, dcterms:created, vault:tag, vault:status))
    }
} GROUP BY ?type ORDER BY DESC(?orphans)
SPARQL
)
```

Report total orphan count and breakdown by type. Over 50% orphans → **Warning** at vault level.

**C2. Dangling References** — Edges pointing to URIs that don't exist:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?pred (COUNT(?target) AS ?dangles) WHERE {
    ?src ?pred ?target .
    FILTER(?pred IN (vault:up, vault:concept, vault:source, vault:extends,
                     vault:supports, vault:criticizes, vault:related))
    FILTER(isIRI(?target))
    FILTER NOT EXISTS { ?target dcterms:title ?t }
} GROUP BY ?pred ORDER BY DESC(?dangles)
SPARQL
)
```

Separate Readwise phantoms (URIs containing `twitter`, `kindle`, `medium`, `reader`) from real broken refs. Real broken refs → **Warning**. Readwise phantoms → **Info**.

**C3. Discoverability Distribution** — How many notes meet the ≥3 incoming link threshold:

Report buckets: orphan (0), under-threshold (1-2), healthy (3-9), hub (10+).

**C4. Hub Distribution** — Top 25 most-connected notes (use existing `vq:hub-notes`).

### Check D: Area Coverage

**D1. Cold Areas** — Areas of focus with few notes serving them:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?areaTitle (COUNT(DISTINCT ?note) AS ?notes) WHERE {
    ?area a vault:Area .
    ?area dcterms:title ?areaTitle .
    OPTIONAL {
        ?note vault:area ?area .
        FILTER(BOUND(?note))
    }
} GROUP BY ?areaTitle ORDER BY ?notes
SPARQL
)
```

Areas with 0 notes → **Warning**. Areas with <5 → **Info**.

### Check E: Freshness

**E1. Stale Notes** — Resource notes not modified in >6 months:

```bash
# Get all resource notes
find "03 - Resources/" -name "*.md" | wc -l
# Get recently modified ones
git log --diff-filter=M --name-only --since="6 months ago" --pretty=format: -- "03 - Resources/" | sort -u | wc -l
```

Report count and percentage. Over 30% stale → **Info**.

### Check F: Branching Factor (Fano Bound)

**Theoretical basis**: Hierarchical navigation has a formal information-theoretic ceiling on branching factor derived from **Fano's inequality**. With a realistic mutual-information budget of ~2 bits per routing decision, to achieve <15% routing error the branching factor $n_k$ at each level must satisfy:

$$n_k \leq 2^{(B+1)/0.85} \approx 11.5$$

**Empirical evidence**: [Hu et al. 2026 (xMemory)](https://arxiv.org/abs/2602.02007) uses a split threshold of 12 and produces an average branching factor of ~4.5 in practice. **Nodes with more than ~12 direct children are routing-unreliable** — an agent navigating such a node faces a classification problem the mutual information budget cannot solve. This applies to **any hierarchical navigation structure**: MOC sections, index subsections, folders treated as namespaces, and concept hubs.

See `[[Bounded Branching - Why This Skill Checks the Fano Bound]]` in `03 - Resources/Obsidian Reference/` for the full background and methodology rationale.

**Why we check this**: a vault that violates this principle in its own navigation structure is inconsistent with the structure-first memory thesis it implements. Check F surfaces violations as structural-integrity warnings so the curator (human or AI) can act on them.

**F1. MOC Section Branching** — Count direct `- [[` entries per `##` heading in MOC files:

```bash
# For each MOC, count entries per top-level section heading
for moc in $(find "03 - Resources/" -name "*MOC*.md"); do
    echo "=== $moc ==="
    awk '
        /^## / { section=$0; count=0; next }
        /^- \[\[/ { count++ }
        END { if (section) print section ": " count }
    ' "$moc"
done
```

Alternative quick check:
```bash
# Total direct entries per MOC file
for moc in $(find "03 - Resources/" -name "*MOC*.md"); do
    total=$(grep -c "^- \[\[" "$moc")
    echo "$moc: $total entries"
done
```

**Severity mapping**:
- $n_k > 12$: **Warning** — Fano bound exceeded; routing becomes unreliable
- $n_k > 25$: **Error** — routing is effectively broken; split immediately
- $n_k > 50$: **Error (critical)** — the node functions as a flat index, not a hub; the pattern layer is absent

**F2. Sub-Index Branching** — Count entries per section in LITERATURE-INDEX, PEOPLE-INDEX, or other sub-indexes:

```bash
# Count entries per ### subsection in LITERATURE-INDEX
awk '
    /^### / { if (section) print section ": " count; section=$0; count=0; next }
    /^- \[\[/ { count++ }
    END { if (section) print section ": " count }
' "03 - Resources/Literature/LITERATURE-INDEX.md"
```

Apply the same severity thresholds as F1. Over-bound sub-sections are candidates for splitting into further subsections with more specific headings.

**F3. Folder-Level Branching** — Folders treated as navigational namespaces (e.g., `Literature/`, any thematic topic folder) should be checked for child count:

```bash
for dir in "03 - Resources/Literature" \
           "03 - Resources/People" \
           $(find "03 - Resources/" -type d -not -path "*/Obsidian Reference*" -mindepth 1 -maxdepth 2); do
    count=$(ls "$dir"/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 12 ]; then
        echo "$dir: $count files"
    fi
done
```

Folders serving as flat namespaces with more than ~50 direct children are in **critical** territory. They should be split into topical subfolders or replaced with sub-indexes that structure the children into bounded groups.

**F4. Concept Node In-Degree** — Concept notes that serve as hubs for many incoming edges are also subject to the Fano bound on the *reverse* direction: an agent navigating incoming references must solve a classification problem over the neighbors. Count `concept:` incoming edges per concept:

```bash
arq --data=scripts/kg/vault-graph-full.ttl --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?conceptTitle (COUNT(?source) AS ?incoming) WHERE {
    ?source vault:concept ?concept .
    ?concept dcterms:title ?conceptTitle .
} GROUP BY ?conceptTitle
HAVING (COUNT(?source) > 12)
ORDER BY DESC(?incoming)
SPARQL
)
```

Concept notes with >12 incoming `concept:` references are candidates for splitting into sub-concepts or promoting to a MOC with explicit intermediate structure.

### Report Format

```
## Vault Health Report — YYYY-MM-DD

### Summary
| Metric | Value |
|--------|-------|
| Total typed notes | N |
| Errors | N |
| Warnings | N |
| Info items | N |

### SHACL Validation
| Severity | Count |
|----------|-------|
| Violations | N |
| Warnings | N |
| Info | N |

Top violations: ...

### Errors
1. **[Type]** N notes with non-canonical types: transcription (N), daily (N), ...
2. **[Hierarchy]** N notes missing required `up:` field
3. **[Branching]** N nodes over the critical Fano bound (>25 direct children)

### Warnings
1. **[Orphans]** N notes (X%) with no incoming edges
2. **[Dangling]** N real broken references (excluding N Readwise phantoms)
3. **[Template]** N notes missing expected fields for their type
4. **[Cold Areas]** N areas with 0 notes serving them
5. **[Branching]** N nodes over the Fano bound (>12 direct children) — routing-unreliable per the structure-first memory thesis. See `[[Bounded Branching - Why This Skill Checks the Fano Bound]]`.

### Info
1. **[Readwise]** N phantom references (twitter: N, kindle: N, ...)
2. **[Stale]** N resource notes not modified in 6+ months (X%)
3. **[Discoverability]** N% orphan, N% under threshold, N% healthy, N% hub
```

---

## Session Mode (`/audit session`)

Scoped to notes changed this session. Lightweight and fast.

### Step 1: Scope from Git

```bash
# Find the first commit from today
SESSION_START=$(git log --since="today 00:00" --reverse --format="%H" | head -1)

# If a session start commit is known, use it
git diff --name-only $SESSION_START -- "*.md"

# Fallback: if no commits today, use HEAD~5 (typical session size)
git diff --name-only HEAD~5 -- "*.md"
```

**How to pick N**: If the session start commit is known (e.g., from a daily note or the first commit message today), diff against that. Otherwise, use `HEAD~5` as a reasonable default for a typical session. For long sessions (20+ commits), use the `--since="today 00:00"` approach instead of counting backwards.

### Step 1.5: SHACL Validation (session-scoped)

If `validation-summary.txt` exists (written by `rebuild-async.sh` after the last `/encode` commit), read it and filter for violations involving the session's changed files. This gives SHACL feedback scoped to what was just created:

```bash
# Read the summary
cat scripts/kg/validation-summary.txt

# For detailed violations on specific notes, grep the full report
for note in $CHANGED_NOTES; do
    slug=$(echo "$note" | sed 's/ /-/g' | sed 's/\.md//')
    grep "$slug" scripts/kg/validation-report.ttl 2>/dev/null | head -5
done
```

If the summary is stale or missing, skip this step — session mode should be fast. The full `/audit` standalone mode will catch it.

### Step 2: Per-Note Checks

For each changed `.md` file, read frontmatter and check:

| Check | How | Severity |
|-------|-----|----------|
| Type canonical? | Compare against list | Error if non-canonical |
| `up:` present? | Read frontmatter | Warning if missing |
| Expected fields? | Check against type template | Warning if missing |
| Edge targets valid? | For `concept:`, `source:`, `extends:` — verify target notes exist and have appropriate types | Warning if domain/range mismatch |
| Orphan? | Grep vault for wikilinks to this note | Info if 0 incoming |
| Branching impact? | If the change added to a MOC section or index, re-check that node's branching factor against Fano bound ($n_k \leq 12$) | Warning if push above bound; Error if above 25 |
| Discoverable? | Count incoming links | Info if <3 |

### Step 3: Session Coherence

- Do all new notes share a MOC? (Check `up:` targets)
- Do new notes link to each other? (Check cross-references)
- Were any notes created but not wired (no MOC listing)?

### Step 4: Session Report

```
## Session Health Check — YYYY-MM-DD

**Scope**: N files changed (N new, N modified)

| Note | Type | up: | Template | Incoming | Status |
|------|------|-----|----------|----------|--------|
| [[Note A]] | concept-note | ✓ | ✓ | 0 | ⚠ orphan |
| [[Note B]] | literature-note | ✓ | ⚠ no year | 4 | ✓ healthy |

**Coherence**: N/N notes share [[MOC Name]]. N cross-links between session notes.
**Issues**: N errors, N warnings
```

---

## When NOT to Use Audit

- **Individual note quality**: Use `/review-note` (4-agent adversarial review)
- **Ontology vocabulary proposals**: Use `/vault-curator review`
- **Vocabulary evolution**: Use `/vault-curator evolve`
- **Session reflection**: Use `/session-retro` (ADHD scaffolding — Audit provides facts, retro provides reflection)

---

## Reference Files

| File | Role |
|------|------|
| `scripts/kg/vault-graph-full.ttl` | Graph data for SPARQL checks |
| `scripts/kg/vault-shapes.ttl` | SHACL shapes (formal constraints) |
| `scripts/kg/validation-report.ttl` | Full SHACL validation report (generated) |
| `scripts/kg/validation-summary.txt` | Human-readable summary (generated by `rebuild-async.sh`) |
| `scripts/kg/vault-queries.ttl` | Query catalog (SIB/UniProt pattern) |
| `scripts/kg/sparql/` | Standalone `.rq` files extracted from catalog |
| `scripts/kg/vault-ontology.ttl` | SKOS + RDFS vocabulary (source of truth) |
| `03 - Resources/Obsidian Reference/Vault Vocabulary.md` | Canonical type list (human-readable view) |
| `.claude/rules/typed-relationships.md` | Domain/range constraints for edge validation |
