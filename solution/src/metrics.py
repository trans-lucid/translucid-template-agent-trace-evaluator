from __future__ import annotations

from collections import Counter

from .trace_schema import AgentTrace, ExpectedTool, TraceStep


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
    if not trace.expected_tools:
        return 1.0
    calls = [step for step in trace.steps if step.type == "tool_call"]
    matched = 0
    for expected in trace.expected_tools:
        if any(_tool_matches(call, expected) for call in calls):
            matched += 1
    order_score = _ordered_tool_score(calls, trace.expected_tools)
    coverage = matched / len(trace.expected_tools)
    return round(0.75 * coverage + 0.25 * order_score, 4)


def evidence_score(trace: AgentTrace) -> float:
    if not trace.requires_evidence:
        return 1.0
    evidence_ids = {step.evidence_id for step in trace.steps if step.evidence_id}
    final_steps = [step for step in trace.steps if step.type == "final"]
    cited = {citation for step in final_steps for citation in step.citations}
    if not evidence_ids:
        return 0.0
    if not cited:
        return 0.0
    return 1.0 if cited.issubset(evidence_ids) else 0.25


def loop_score(trace: AgentTrace) -> float:
    failed_calls = [
        (step.tool_name, tuple(sorted(step.arguments.items())))
        for step in trace.steps
        if step.type == "tool_call" and step.status == "error"
    ]
    if not failed_calls:
        return 1.0
    worst_repeat = max(Counter(failed_calls).values())
    if worst_repeat >= 3:
        return 0.0
    if worst_repeat == 2:
        return 0.5
    return 1.0


def escalation_score(trace: AgentTrace) -> float:
    if not trace.should_escalate:
        return 1.0
    combined = " ".join([trace.final_answer, *(step.text for step in trace.steps)]).lower()
    return 1.0 if "escalat" in combined or "handoff" in combined else 0.0


def _tool_matches(call: TraceStep, expected: ExpectedTool) -> bool:
    if call.tool_name != expected.name:
        return False
    return all(call.arguments.get(key) == value for key, value in expected.args_subset.items())


def _ordered_tool_score(calls: list[TraceStep], expected_tools: list[ExpectedTool]) -> float:
    if not expected_tools:
        return 1.0
    cursor = 0
    for call in calls:
        if cursor >= len(expected_tools):
            break
        if _tool_matches(call, expected_tools[cursor]):
            cursor += 1
    return cursor / len(expected_tools)
