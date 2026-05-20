#!/usr/bin/env bash
set -euo pipefail

TARGET="${EVAL_TARGET:-$(pwd)/solution}"
EVAL_TARGET="$TARGET" python3 -m pytest evaluator/tests_hidden

