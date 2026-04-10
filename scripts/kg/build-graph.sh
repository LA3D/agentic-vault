#!/bin/bash
# build-graph.sh — Full pipeline: vault notes → JSON-LD → Turtle → materialize → validate
# Usage: ./build-graph.sh [--stats] [--skip-validate] [--skip-materialize]
#
# Outputs:
#   scripts/kg/vault-graph.jsonld      (intermediate JSON-LD)
#   scripts/kg/vault-graph.ttl         (base Turtle graph)
#   scripts/kg/vault-graph-full.ttl    (base + materialized triples)
#   scripts/kg/validation-report.ttl   (SHACL validation report)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
JSONLD_OUT="$SCRIPT_DIR/vault-graph.jsonld"
TURTLE_OUT="$SCRIPT_DIR/vault-graph.ttl"
FULL_OUT="$SCRIPT_DIR/vault-graph-full.ttl"
SHAPES="$SCRIPT_DIR/vault-shapes.ttl"
REPORT_OUT="$SCRIPT_DIR/validation-report.ttl"

STATS_FLAG=""
SKIP_VALIDATE=""
SKIP_MATERIALIZE=""
for arg in "$@"; do
    case "$arg" in
        --stats) STATS_FLAG="--stats" ;;
        --skip-validate) SKIP_VALIDATE=1 ;;
        --skip-materialize) SKIP_MATERIALIZE=1 ;;
    esac
done

echo "=== Vault Knowledge Graph Build ===" >&2
echo "Vault: $VAULT_ROOT" >&2
echo "" >&2

# Step 1: Extract frontmatter → JSON-LD
echo "Step 1: Extracting frontmatter → JSON-LD..." >&2
python3 "$SCRIPT_DIR/vault-to-jsonld.py" \
    --vault "$VAULT_ROOT" \
    --output "$JSONLD_OUT" \
    $STATS_FLAG

echo "" >&2

# Step 2: Convert JSON-LD → Turtle via riot
echo "Step 2: Converting JSON-LD → Turtle via riot..." >&2
riot --syntax=jsonld --output=turtle "$JSONLD_OUT" 2>/dev/null > "$TURTLE_OUT"

echo "Turtle written to $TURTLE_OUT" >&2
echo "Lines in Turtle: $(wc -l < "$TURTLE_OUT" | tr -d ' ')" >&2
echo "" >&2

# Step 3: Materialize implied triples via CONSTRUCT queries
# Each query outputs N-Triples (no prefix conflicts when concatenating)
if [[ -z "$SKIP_MATERIALIZE" ]]; then
    echo "Step 3: Materializing implied triples..." >&2
    INFERRED=$(mktemp)

    run_construct() {
        arq --data="$TURTLE_OUT" --query=<(echo "$1") 2>/dev/null | \
            riot --syntax=turtle --output=ntriples 2>/dev/null >> "$INFERRED"
    }

    # Area inheritance: propagate area down up: hierarchy
    run_construct 'PREFIX vault: <https://example.com/vault/ontology#>
CONSTRUCT { ?note vault:area ?area }
WHERE {
    ?note vault:up+ ?ancestor .
    ?ancestor vault:area ?area .
    FILTER NOT EXISTS { ?note vault:area ?area }
}'

    # Inverse supports
    run_construct 'PREFIX vault: <https://example.com/vault/ontology#>
CONSTRUCT { ?target vault:supportedBy ?source }
WHERE { ?source vault:supports ?target }'

    # Inverse criticizes
    run_construct 'PREFIX vault: <https://example.com/vault/ontology#>
CONSTRUCT { ?target vault:criticizedBy ?source }
WHERE { ?source vault:criticizes ?target }'

    # Inverse concept
    run_construct 'PREFIX vault: <https://example.com/vault/ontology#>
CONSTRUCT { ?target vault:conceptOf ?source }
WHERE { ?source vault:concept ?target }'

    # Hub detection
    run_construct 'PREFIX vault: <https://example.com/vault/ontology#>
CONSTRUCT { ?note vault:isHub true }
WHERE {
    { SELECT ?note (COUNT(?src) AS ?inbound) WHERE {
        ?src ?pred ?note .
        FILTER(?pred IN (vault:up, vault:area, vault:concept, vault:source,
                         vault:extends, vault:supports, vault:criticizes,
                         vault:implementation, vault:related))
    } GROUP BY ?note }
    FILTER(?inbound >= 10)
}'

    INFERRED_COUNT=$(wc -l < "$INFERRED" | tr -d ' ')
    echo "Materialized ~${INFERRED_COUNT} triples" >&2

    # Merge: convert inferred N-Triples to Turtle, then concatenate
    # arq can load multiple --data files, so we keep them separate for querying
    # For the combined file, append N-Triples after the base Turtle
    # (N-Triples are valid at the end of a Turtle file since Turtle is a superset)
    cp "$TURTLE_OUT" "$FULL_OUT"
    echo "" >> "$FULL_OUT"
    echo "# --- Materialized triples ---" >> "$FULL_OUT"
    cat "$INFERRED" >> "$FULL_OUT"
    rm "$INFERRED"

    echo "Full graph written to $FULL_OUT" >&2
    echo "Lines in full graph: $(wc -l < "$FULL_OUT" | tr -d ' ')" >&2
    echo "" >&2
fi

# Step 4: SHACL validation
if [[ -z "$SKIP_VALIDATE" ]]; then
    echo "Step 4: SHACL validation..." >&2
    VALIDATE_DATA="${FULL_OUT}"
    [[ -n "$SKIP_MATERIALIZE" ]] && VALIDATE_DATA="$TURTLE_OUT"

    shacl validate --shapes="$SHAPES" --data="$VALIDATE_DATA" > "$REPORT_OUT" 2>&1

    # Summary
    VIOLATIONS=$(grep -c "sh:Violation" "$REPORT_OUT" || true)
    WARNINGS=$(grep -c "sh:Warning" "$REPORT_OUT" || true)
    INFOS=$(grep -c "sh:Info" "$REPORT_OUT" || true)
    echo "Validation report: $REPORT_OUT" >&2
    if grep -q "sh:conforms  true" "$REPORT_OUT"; then
        echo "Result: CONFORMS" >&2
    else
        echo "Result: ${VIOLATIONS} violations, ${WARNINGS} warnings, ${INFOS} info" >&2
    fi
    echo "" >&2
fi

# Step 5: Quick stats query
echo "Step 5: Type distribution..." >&2
QUERY_DATA="${FULL_OUT}"
[[ -n "$SKIP_MATERIALIZE" ]] && QUERY_DATA="$TURTLE_OUT"

arq --data="$QUERY_DATA" --query=<(cat <<'SPARQL'
PREFIX vault: <https://example.com/vault/ontology#>
SELECT ?type (COUNT(?note) AS ?count) WHERE {
    ?note a ?type .
} GROUP BY ?type ORDER BY DESC(?count)
SPARQL
) 2>&1

echo "" >&2
echo "=== Done ===" >&2
