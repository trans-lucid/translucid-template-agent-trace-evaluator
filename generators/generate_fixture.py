#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


TOOLS = ["lookup_invoice", "issue_refund", "query_status", "lookup_order"]


def build_trace(index: int, rng: random.Random) -> dict:
    invoice_id = f"INV-{1000 + index}"
    tool = rng.choice(TOOLS)
    return {
        "trace_id": f"generated_run_{index:03d}",
        "task": f"Resolve account issue {invoice_id}",
        "expected_final_contains": [invoice_id],
        "expected_tools": [{"name": tool, "args_subset": {"id": invoice_id}}],
        "requires_evidence": True,
        "should_escalate": rng.random() < 0.2,
        "max_latency_ms": 2500,
        "max_cost_usd": 0.05,
        "final_answer": f"Handled {invoice_id}.",
        "latency_ms": rng.randint(800, 4000),
        "cost_usd": round(rng.uniform(0.01, 0.08), 4),
        "steps": [
            {"step_id": "s1", "type": "tool_call", "tool_name": tool, "arguments": {"id": invoice_id}, "status": "ok"},
            {"step_id": "s2", "type": "observation", "text": f"evidence for {invoice_id}", "evidence_id": f"ev-{invoice_id}"},
            {"step_id": "s3", "type": "final", "text": f"Handled {invoice_id}.", "citations": [f"ev-{invoice_id}"]},
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260519)
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(json.dumps(build_trace(i, rng), sort_keys=True) for i in range(args.count)) + "\n")


if __name__ == "__main__":
    main()

