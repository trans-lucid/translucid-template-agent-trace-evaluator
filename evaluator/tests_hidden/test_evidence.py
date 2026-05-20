from __future__ import annotations

from .load_target import score


def test_correct_tool_path_without_evidence_is_penalized():
    result = score(
        {
            "trace_id": "hidden_no_evidence",
            "task": "Explain tenant beta outage",
            "expected_final_contains": ["tenant beta", "rate limit"],
            "expected_tools": [{"name": "query_status", "args_subset": {"tenant": "beta"}}],
            "requires_evidence": True,
            "should_escalate": False,
            "max_latency_ms": 2500,
            "max_cost_usd": 0.05,
            "final_answer": "Tenant beta is rate limited.",
            "latency_ms": 800,
            "cost_usd": 0.01,
            "steps": [
                {"step_id": "s1", "type": "tool_call", "tool_name": "query_status", "arguments": {"tenant": "beta"}, "status": "ok"},
                {"step_id": "s2", "type": "observation", "text": "rate limit active for tenant beta"},
                {"step_id": "s3", "type": "final", "text": "Tenant beta is rate limited.", "citations": []},
            ],
        }
    )
    if result.evidence > 0.4:
        raise AssertionError("missing_evidence_not_penalized")

