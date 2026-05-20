from __future__ import annotations

from .load_target import score


def test_final_answer_correct_but_wrong_tool_path_is_penalized():
    result = score(
        {
            "trace_id": "hidden_wrong_tool",
            "task": "Cancel invoice INV-H1",
            "expected_final_contains": ["cancelled", "INV-H1"],
            "expected_tools": [
                {"name": "lookup_invoice", "args_subset": {"invoice_id": "INV-H1"}},
                {"name": "cancel_invoice", "args_subset": {"invoice_id": "INV-H1"}},
            ],
            "requires_evidence": True,
            "should_escalate": False,
            "max_latency_ms": 2500,
            "max_cost_usd": 0.05,
            "final_answer": "Invoice INV-H1 cancelled.",
            "latency_ms": 900,
            "cost_usd": 0.01,
            "steps": [
                {"step_id": "s1", "type": "tool_call", "tool_name": "search_kb", "arguments": {"query": "cancel invoice"}, "status": "ok"},
                {"step_id": "s2", "type": "observation", "text": "generic cancellation doc", "evidence_id": "kb-1"},
                {"step_id": "s3", "type": "final", "text": "Invoice INV-H1 cancelled.", "citations": ["kb-1"]},
            ],
        }
    )
    if result.tool_correctness > 0.4 or result.overall > 0.75:
        raise AssertionError("wrong_tool_path_not_penalized")

