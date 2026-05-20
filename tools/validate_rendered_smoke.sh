#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -d "$ROOT/generated/main" ] || [ ! -d "$ROOT/generated/solution" ]; then
  python3 "$ROOT/tools/render_template.py"
fi

python3 "$ROOT/tools/scan_safety.py" "$ROOT/generated/main"

cd "$ROOT/generated/main"
set +e
MAIN_OUTPUT="$(python3 -m pytest tests/public/test_public.py 2>&1)"
MAIN_STATUS=$?
set -e
printf '%s\n' "$MAIN_OUTPUT"
if [ "$MAIN_STATUS" -eq 0 ]; then
  echo "rendered main unexpectedly passed starter public tests" >&2
  exit 1
fi
if ! grep -Eq "wrong_tool_path_not_penalized|missing_evidence_not_penalized|loop_not_detected" <<<"$MAIN_OUTPUT"; then
  echo "rendered main failed without an expected marker" >&2
  exit 1
fi

cd "$ROOT/generated/solution"
EVAL_TARGET="$PWD/solution" python3 -m pytest tests/public/test_public.py evaluator/tests_hidden solution/tests

echo "rendered smoke validation passed"
