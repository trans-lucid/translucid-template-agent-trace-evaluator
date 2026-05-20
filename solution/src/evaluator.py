from __future__ import annotations

from dataclasses import asdict, dataclass

from .metrics import (
    cost_score,
    escalation_score,
    evidence_score,
    final_answer_score,
    latency_score,
    loop_score,
    tool_correctness_score,
)
from .trace_schema import AgentTrace


@dataclass(frozen=True)
class TraceScore:
    trace_id: str
    overall: float
    final_answer: float
    tool_correctness: float
    evidence: float
    loop: float
    escalation: float
    latency: float
    cost: float
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def score_trace(trace: AgentTrace) -> TraceScore:
    final = final_answer_score(trace)
    tool = tool_correctness_score(trace)
    evidence = evidence_score(trace)
    loop = loop_score(trace)
    escalation = escalation_score(trace)
    latency = latency_score(trace)
    cost = cost_score(trace)
    overall = round(
        0.15 * final
        + 0.35 * tool
        + 0.25 * evidence
        + 0.10 * loop
        + 0.05 * escalation
        + 0.05 * latency
        + 0.05 * cost,
        4,
    )
    return TraceScore(
        trace_id=trace.trace_id,
        overall=overall,
        final_answer=round(final, 4),
        tool_correctness=round(tool, 4),
        evidence=round(evidence, 4),
        loop=round(loop, 4),
        escalation=round(escalation, 4),
        latency=round(latency, 4),
        cost=round(cost, 4),
        warnings=trace.warnings,
    )


def evaluate_traces(traces: list[AgentTrace]) -> list[TraceScore]:
    return [score_trace(trace) for trace in traces]
