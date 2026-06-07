#!/usr/bin/env bash
set -euo pipefail

if ! find evaluator/tests_hidden -name 'test_*.py' -print -quit | grep -q .; then
  echo "no hidden tests discovered" >&2
  exit 1
fi
if [ -d "$(pwd)/src" ]; then
  TARGET="${EVAL_TARGET:-$(pwd)}"
else
  TARGET="${EVAL_TARGET:-$(pwd)/solution}"
fi
EVAL_TARGET="$TARGET" python3 -m pytest evaluator/tests_hidden
