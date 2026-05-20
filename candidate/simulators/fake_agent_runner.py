from __future__ import annotations

import json
import os
from pathlib import Path

from otel_trace_sender import build_zipkin_spans, post_with_retry


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    trace_file = ROOT / "traces" / "public_runs.jsonl"
    traces = [json.loads(line) for line in trace_file.read_text().splitlines() if line.strip()]
    spans = build_zipkin_spans(traces)
    post_with_retry(os.environ.get("JAEGER_ZIPKIN_URL", "http://localhost:9411/api/v2/spans"), spans)
    print(f"emitted {len(spans)} spans")


if __name__ == "__main__":
    main()
