from __future__ import annotations

import urllib.request
import json
from pathlib import Path

from .load_target import import_from_target


TRACE_API_URL = "http://localhost:8089"


def wait_for_trace_api() -> None:
    last_error: Exception | None = None
    import time

    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{TRACE_API_URL}/healthz", timeout=2) as response:  # noqa: S310 - local simulator URL
                if response.status == 200:
                    return
        except Exception as exc:  # pragma: no cover - only used while waiting
            last_error = exc
        time.sleep(0.5)
    raise RuntimeError(f"trace_api_not_ready:{last_error}")


def test_docker_trace_api_path_detects_expected_starter_failure(tmp_path: Path):
    wait_for_trace_api()
    emit_request = urllib.request.Request(f"{TRACE_API_URL}/emit/public", method="POST")
    with urllib.request.urlopen(emit_request, timeout=10) as response:  # noqa: S310
        emitted = json.loads(response.read().decode("utf-8"))
    assert emitted["emitted_spans"] >= 8
    assert emitted["jaeger_post_success"] is True

    trace_file = tmp_path / "fetched.jsonl"
    with urllib.request.urlopen(f"{TRACE_API_URL}/traces/public", timeout=5) as response:  # noqa: S310
        trace_file.write_bytes(response.read())

    schema = import_from_target("src.trace_schema")
    evaluator = import_from_target("src.evaluator")
    traces = schema.load_traces(trace_file)
    scores = {score.trace_id: score for score in evaluator.evaluate_traces(traces)}

    wrong_tool = scores["run_wrong_tool_final_correct"]
    if wrong_tool.tool_correctness > 0.4:
        raise AssertionError("wrong_tool_path_not_penalized")
