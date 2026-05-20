from __future__ import annotations

from .load_target import score


def test_repeated_failed_tool_loop_and_missing_escalation_are_penalized():
    result = score(
        {
            "trace_id": "hidden_loop_escalate",
            "task": "Find high-risk account owner",
            "expected_final_contains": ["escalated"],
            "expected_tools": [{"name": "lookup_account_owner", "args_subset": {"account_id": "A-9"}}],
            "requires_evidence": False,
            "should_escalate": True,
            "max_latency_ms": 2000,
            "max_cost_usd": 0.04,
            "final_answer": "The owner is probably Maya.",
            "latency_ms": 4700,
            "cost_usd": 0.09,
            "steps": [
                {"step_id": "s1", "type": "tool_call", "tool_name": "lookup_account_owner", "arguments": {"account_id": "A-9"}, "status": "error"},
                {"step_id": "s2", "type": "tool_call", "tool_name": "lookup_account_owner", "arguments": {"account_id": "A-9"}, "status": "error"},
                {"step_id": "s3", "type": "tool_call", "tool_name": "lookup_account_owner", "arguments": {"account_id": "A-9"}, "status": "error"},
                {"step_id": "s4", "type": "final", "text": "The owner is probably Maya.", "citations": []},
            ],
        }
    )
    if result.loop > 0.3:
        raise AssertionError("loop_not_detected")
    if result.escalation > 0.3:
        raise AssertionError("escalation_not_penalized")

