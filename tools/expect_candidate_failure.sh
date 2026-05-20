#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/candidate"

set +e
OUTPUT="$(python3 -m pytest tests/public/test_public.py 2>&1)"
STATUS=$?
set -e

printf '%s\n' "$OUTPUT"

if [ "$STATUS" -eq 0 ]; then
  echo "expected candidate starter to fail public tests, but it passed" >&2
  exit 1
fi

if grep -Eq "wrong_tool_path_not_penalized|missing_evidence_not_penalized|loop_not_detected|escalation_not_penalized" <<<"$OUTPUT"; then
  echo "candidate starter failed for expected public marker"
  exit 0
fi

echo "candidate starter failed, but not for an expected marker" >&2
exit 1

