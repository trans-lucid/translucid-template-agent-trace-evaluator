from __future__ import annotations

import json
from pathlib import Path

from .evaluator import TraceScore


def build_report(scores: list[TraceScore]) -> dict[str, object]:
    score_dicts = [score.to_dict() for score in scores]
    average = round(sum(score.overall for score in scores) / max(len(scores), 1), 4)
    return {
        "summary": {
            "trace_count": len(scores),
            "average_overall": average,
        },
        "scores": score_dicts,
    }


def write_report(scores: list[TraceScore], out: str | Path, summary: str | Path | None = None) -> dict[str, object]:
    report = build_report(scores)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n")
    if summary:
        summary_path = Path(summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(
            f"# Agent Trace Evaluation\n\nTraces: {report['summary']['trace_count']}\n\nAverage: {report['summary']['average_overall']}\n"
        )
    return report

