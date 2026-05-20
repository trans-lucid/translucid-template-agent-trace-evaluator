from __future__ import annotations

import sys
from pathlib import Path

solution_root = Path(__file__).resolve().parents[1]
if str(solution_root) in sys.path:
    sys.path.remove(str(solution_root))
sys.path.insert(0, str(solution_root))

from src.evaluator import evaluate_traces
from src.trace_schema import load_traces


def test_reference_solution_scores_public_edge_cases():
    trace_path = Path("candidate/traces/public_runs.jsonl")
    if not trace_path.exists():
        trace_path = Path("traces/public_runs.jsonl")
    scores = {score.trace_id: score for score in evaluate_traces(load_traces(trace_path))}
    assert scores["run_good_refund"].overall >= 0.85
    assert scores["run_wrong_tool_final_correct"].tool_correctness <= 0.4
    assert scores["run_missing_evidence"].evidence <= 0.4
    assert scores["run_tool_loop"].loop <= 0.3
