#!/bin/bash
# Run synchronously, or launch in the background and wait for the process.
# A busy lock is an error: callers must not assume the graph is fresh.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCKDIR="$SCRIPT_DIR/.rebuild.lock"
if ! mkdir "$LOCKDIR" 2>/dev/null; then
    echo "KG build busy; wait for the active build and verify its result" >&2
    exit 75
fi
trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT
for tool in python3 riot arq shacl; do
    command -v "$tool" >/dev/null || { echo "Missing dependency: $tool" >&2; exit 127; }
done
python3 -c 'import yaml' || { echo "Install PyYAML in your Python environment" >&2; exit 1; }
"$SCRIPT_DIR/build-graph.sh" --stats "$@"
if [[ " $* " != *" --skip-validate "* ]]; then
    python3 - "$SCRIPT_DIR/validation-report.ttl" "$SCRIPT_DIR/validation-summary.txt" <<'PYCODE'
import pathlib, re, sys
report = pathlib.Path(sys.argv[1]).read_text()
conforms = bool(re.search(r'sh:conforms\s+true', report))
lines = ['# SHACL Validation Summary', 'STATUS: ' + ('CONFORMS' if conforms else 'NON-CONFORMING')]
for label, severity in [('VIOLATIONS', 'Violation'), ('WARNINGS', 'Warning'), ('INFO', 'Info')]:
    count = len(re.findall(r"sh:" + severity + r"\b", report))
    lines.append(f"{label}: {count}")
pathlib.Path(sys.argv[2]).write_text('\n'.join(lines) + '\n')
PYCODE
fi
