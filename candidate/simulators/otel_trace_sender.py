from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from typing import Any


def _hex_id(value: str, length: int) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]


def build_zipkin_spans(raw_traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    now_us = int(time.time() * 1_000_000)
    for trace_index, trace in enumerate(raw_traces):
        trace_id = _hex_id(str(trace.get("trace_id", f"trace-{trace_index}")), 32)
        root_id = _hex_id(f"{trace_id}:root", 16)
        root_start = now_us + trace_index * 1_000_000
        spans.append(
            {
                "traceId": trace_id,
                "id": root_id,
                "name": "agent.run",
                "timestamp": root_start,
                "duration": int(trace.get("latency_ms", 1) * 1000),
                "localEndpoint": {"serviceName": "support-agent"},
                "tags": {
                    "agent.trace_id": str(trace.get("trace_id", "unknown-trace")),
                    "agent.task": str(trace.get("task", "")),
                    "agent.cost_usd": str(trace.get("cost_usd", 0.0)),
                },
            }
        )
        for step_index, step in enumerate(trace.get("steps") or []):
            step_id = str(step.get("step_id") or f"step-{step_index}")
            spans.append(
                {
                    "traceId": trace_id,
                    "id": _hex_id(f"{trace_id}:{step_id}", 16),
                    "parentId": root_id,
                    "name": f"agent.{step.get('type', 'unknown')}",
                    "timestamp": root_start + (step_index + 1) * 10_000,
                    "duration": max(1, int(step.get("ended_at_ms", 1) - step.get("started_at_ms", 0))) * 1000,
                    "localEndpoint": {"serviceName": "support-agent"},
                    "tags": {
                        "agent.step_id": step_id,
                        "agent.type": str(step.get("type", "unknown")),
                        "agent.tool_name": str(step.get("tool_name", "")),
                        "agent.status": str(step.get("status", "")),
                    },
                }
            )
    return spans


def post_zipkin_spans(url: str, spans: list[dict[str, Any]], timeout: float = 2.0) -> None:
    body = json.dumps(spans).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - local simulator URL
        if response.status >= 300:
            raise RuntimeError(f"zipkin_post_failed_{response.status}")


def post_with_retry(url: str, spans: list[dict[str, Any]], retries: int = 20) -> None:
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            post_zipkin_spans(url, spans)
            return
        except (urllib.error.URLError, RuntimeError) as exc:
            last_error = exc
            time.sleep(0.5)
    raise RuntimeError(f"jaeger_not_ready:{last_error}")

