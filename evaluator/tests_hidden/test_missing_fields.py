from __future__ import annotations

from .load_target import parse, score


def test_missing_span_fields_do_not_crash_and_emit_warning():
    raw = {
        "task": "Trace with missing identifiers",
        "expected_final_contains": ["handled"],
        "expected_tools": [],
        "requires_evidence": False,
        "should_escalate": False,
        "final_answer": "handled",
        "steps": [{"type": "final", "text": "handled"}],
    }
    trace = parse(raw)
    result = score(raw)
    assert "missing_trace_id" in trace.warnings
    assert result.trace_id == "unknown-trace"

