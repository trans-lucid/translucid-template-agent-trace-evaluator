from __future__ import annotations

from .trace_schema import AgentTrace


def final_answer_score(trace: AgentTrace) -> float:
    answer = trace.final_answer.lower()
    if not trace.expected_final_contains:
        return 1.0
    matches = sum(1 for token in trace.expected_final_contains if token.lower() in answer)
    return matches / len(trace.expected_final_contains)


def latency_score(trace: AgentTrace) -> float:
    if trace.latency_ms <= trace.max_latency_ms:
        return 1.0
    return max(0.0, 1.0 - ((trace.latency_ms - trace.max_latency_ms) / max(trace.max_latency_ms, 1)))


def cost_score(trace: AgentTrace) -> float:
    if trace.cost_usd <= trace.max_cost_usd:
        return 1.0
    return max(0.0, 1.0 - ((trace.cost_usd - trace.max_cost_usd) / max(trace.max_cost_usd, 0.01)))


def tool_correctness_score(trace: AgentTrace) -> float:
    # Starter bug: tool path correctness is ignored.
    return 1.0


def evidence_score(trace: AgentTrace) -> float:
    # Starter bug: unsupported answers are treated as fully grounded.
    return 1.0


def loop_score(trace: AgentTrace) -> float:
    # Starter bug: repeated failed tool calls are not detected.
    return 1.0


def escalation_score(trace: AgentTrace) -> float:
    # Starter bug: confident answers are not penalized when escalation is required.
    return 1.0

