from __future__ import annotations

import json
from pathlib import Path

from .load_target import import_from_target, load_public_traces


def _scores_by_id():
    evaluator = import_from_target("src.evaluator")
    traces = load_public_traces()
    return {score.trace_id: score for score in evaluator.evaluate_traces(traces)}


def test_trace_parser_handles_public_schema():
    traces = load_public_traces()
    assert len(traces) >= 4
    good = next(trace for trace in traces if trace.trace_id == "run_good_refund")
    assert good.expected_tools[0].name == "lookup_invoice"
    assert good.steps[0].tool_name == "lookup_invoice"


def test_good_trace_scores_high():
    scores = _scores_by_id()
    assert scores["run_good_refund"].overall >= 0.85


def test_wrong_tool_path_is_penalized_even_when_final_answer_is_correct():
    scores = _scores_by_id()
    score = scores["run_wrong_tool_final_correct"]
    if score.tool_correctness > 0.4 or score.overall > 0.7:
        raise AssertionError("wrong_tool_path_not_penalized")


def test_missing_evidence_is_penalized():
    scores = _scores_by_id()
    score = scores["run_missing_evidence"]
    if score.evidence > 0.4 or score.overall > 0.8:
        raise AssertionError("missing_evidence_not_penalized")


def test_repeated_failed_tool_loop_is_detected():
    scores = _scores_by_id()
    score = scores["run_tool_loop"]
    if score.loop > 0.3:
        raise AssertionError("loop_not_detected")


def test_report_is_machine_readable(tmp_path: Path):
    evaluator = import_from_target("src.evaluator")
    report = import_from_target("src.report")
    scores = evaluator.evaluate_traces(load_public_traces())
    out = tmp_path / "report.json"
    report.write_report(scores, out)
    data = json.loads(out.read_text())
    assert data["summary"]["trace_count"] == len(scores)
    assert "scores" in data

