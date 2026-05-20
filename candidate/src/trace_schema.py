from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExpectedTool:
    name: str
    args_subset: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TraceStep:
    step_id: str
    type: str
    tool_name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    status: str | None = None
    text: str = ""
    evidence_id: str | None = None
    citations: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass(frozen=True)
class AgentTrace:
    trace_id: str
    task: str
    final_answer: str
    expected_final_contains: list[str]
    expected_tools: list[ExpectedTool]
    requires_evidence: bool
    should_escalate: bool
    latency_ms: int
    cost_usd: float
    max_latency_ms: int
    max_cost_usd: float
    steps: list[TraceStep]
    warnings: list[str] = field(default_factory=list)


def _step_from_dict(raw: dict[str, Any], index: int) -> TraceStep:
    return TraceStep(
        step_id=str(raw.get("step_id") or f"missing-step-{index}"),
        type=str(raw.get("type") or "unknown"),
        tool_name=raw.get("tool_name"),
        arguments=dict(raw.get("arguments") or {}),
        status=raw.get("status"),
        text=str(raw.get("text") or ""),
        evidence_id=raw.get("evidence_id"),
        citations=list(raw.get("citations") or []),
        error=raw.get("error"),
    )


def parse_trace(raw: dict[str, Any]) -> AgentTrace:
    warnings: list[str] = []
    if "trace_id" not in raw:
        warnings.append("missing_trace_id")
    if "steps" not in raw:
        warnings.append("missing_steps")

    return AgentTrace(
        trace_id=str(raw.get("trace_id") or "unknown-trace"),
        task=str(raw.get("task") or ""),
        final_answer=str(raw.get("final_answer") or ""),
        expected_final_contains=list(raw.get("expected_final_contains") or []),
        expected_tools=[
            ExpectedTool(name=str(tool.get("name")), args_subset=dict(tool.get("args_subset") or {}))
            for tool in raw.get("expected_tools", [])
        ],
        requires_evidence=bool(raw.get("requires_evidence", False)),
        should_escalate=bool(raw.get("should_escalate", False)),
        latency_ms=int(raw.get("latency_ms") or 0),
        cost_usd=float(raw.get("cost_usd") or 0.0),
        max_latency_ms=int(raw.get("max_latency_ms") or 10_000),
        max_cost_usd=float(raw.get("max_cost_usd") or 1.0),
        steps=[_step_from_dict(step, index) for index, step in enumerate(raw.get("steps") or [])],
        warnings=warnings,
    )


def load_traces(path: str | Path) -> list[AgentTrace]:
    traces: list[AgentTrace] = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            traces.append(parse_trace(json.loads(line)))
    return traces

