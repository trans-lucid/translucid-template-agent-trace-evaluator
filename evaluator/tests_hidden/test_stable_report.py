from __future__ import annotations

import json

from .load_target import import_from_target, target_root


def test_report_output_is_stable_machine_readable(tmp_path):
    schema = import_from_target("src.trace_schema")
    evaluator = import_from_target("src.evaluator")
    report = import_from_target("src.report")
    traces = schema.load_traces(target_root() / "traces" / "public_runs.jsonl")
    scores = evaluator.evaluate_traces(traces)
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    report.write_report(scores, first)
    report.write_report(scores, second)
    if first.read_text() != second.read_text():
        raise AssertionError("unstable_report_output")
    assert json.loads(first.read_text())["summary"]["trace_count"] == len(scores)
