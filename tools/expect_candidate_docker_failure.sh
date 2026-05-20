#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/candidate"

cleanup() {
  docker compose down -v >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose up -d

set +e
OUTPUT="$(python3 -m pytest tests/public/test_integration_trace_api.py 2>&1)"
STATUS=$?
set -e

printf '%s\n' "$OUTPUT"

if [ "$STATUS" -eq 0 ]; then
  echo "expected candidate starter to fail Docker-backed integration, but it passed" >&2
  exit 1
fi

if grep -Eq "wrong_tool_path_not_penalized|trace_api_not_ready" <<<"$OUTPUT"; then
  if grep -q "trace_api_not_ready" <<<"$OUTPUT"; then
    echo "Docker integration failed because trace API was not ready" >&2
    exit 1
  fi
  echo "candidate Docker integration failed for expected marker"
  EVAL_TARGET="$ROOT/solution" python3 -m pytest tests/public/test_integration_trace_api.py
  echo "solution Docker integration passed"
  exit 0
fi

echo "candidate Docker integration failed, but not for an expected marker" >&2
exit 1
