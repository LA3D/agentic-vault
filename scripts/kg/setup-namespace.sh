#!/bin/bash
# setup-namespace.sh — Replace the default namespace with your own domain
#
# Usage: ./setup-namespace.sh https://yourdomain.com/vault
#
# This replaces the placeholder namespace (https://example.com/vault)
# across all KG pipeline files: ontology, shapes, queries, context, scripts.
# Run once during vault setup, or again if you change your domain.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <your-namespace-base>"
    echo ""
    echo "Example: $0 https://yourdomain.com/vault"
    echo "         $0 https://example.com/vault  (to reset to default)"
    echo ""
    echo "This will replace the namespace across all KG pipeline files."
    exit 1
fi

NEW_NS="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OLD_NS="https://example.com/vault"

# Validate the namespace looks like a URL
if [[ ! "$NEW_NS" =~ ^https?:// ]]; then
    echo "Error: Namespace should be a URL (e.g., https://yourdomain.com/vault)"
    exit 1
fi

# Strip trailing slash for consistency
NEW_NS="${NEW_NS%/}"

echo "Replacing namespace:"
echo "  Old: $OLD_NS"
echo "  New: $NEW_NS"
echo ""

# Count files to modify
FILES_MODIFIED=0

# Replace in all relevant file types
for file in "$SCRIPT_DIR"/*.jsonld "$SCRIPT_DIR"/*.ttl "$SCRIPT_DIR"/*.py "$SCRIPT_DIR"/*.sh "$SCRIPT_DIR"/sparql/*.rq; do
    if [[ -f "$file" ]] && grep -q "$OLD_NS" "$file" 2>/dev/null; then
        sed -i '' "s|$OLD_NS|$NEW_NS|g" "$file"
        echo "  Updated: $(basename "$file")"
        FILES_MODIFIED=$((FILES_MODIFIED + 1))
    fi
done

# Also update skill files that reference the namespace
SKILLS_DIR="$SCRIPT_DIR/../../.claude/skills"
if [[ -d "$SKILLS_DIR" ]]; then
    for file in $(grep -rl "$OLD_NS" "$SKILLS_DIR" 2>/dev/null); do
        sed -i '' "s|$OLD_NS|$NEW_NS|g" "$file"
        echo "  Updated: $(echo "$file" | sed "s|.*/\.claude/||")"
        FILES_MODIFIED=$((FILES_MODIFIED + 1))
    done
fi

echo ""
echo "Done. Modified $FILES_MODIFIED files."
echo ""
echo "To verify: grep -r 'example.com/vault' scripts/kg/ .claude/skills/"
echo "To rebuild the graph: scripts/kg/build-graph.sh --stats"
