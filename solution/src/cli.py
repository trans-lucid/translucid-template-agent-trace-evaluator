from __future__ import annotations

import argparse
import shutil
import urllib.request
from pathlib import Path

from .evaluator import evaluate_traces
from .report import write_report
from .trace_schema import load_traces


ROOT = Path(__file__).resolve().parents[1]


def fetch_traces(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=10) as response:  # noqa: S310 - local simulator URL
        out.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    seed = sub.add_parser("seed")
    seed.add_argument("--out", type=Path, default=ROOT / "traces" / "public_runs.jsonl")

    fetch = sub.add_parser("fetch")
    fetch.add_argument("--url", default="http://localhost:8089/traces/public")
    fetch.add_argument("--out", type=Path, default=ROOT / "traces" / "public_runs.jsonl")

    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--traces", type=Path, required=True)
    evaluate.add_argument("--out", type=Path, required=True)
    evaluate.add_argument("--summary", type=Path)

    args = parser.parse_args()

    if args.command == "seed":
        source = ROOT / "traces" / "public_runs.jsonl"
        if source.resolve() != args.out.resolve():
            shutil.copy2(source, args.out)
        print(f"seeded {args.out}")
        return

    if args.command == "fetch":
        fetch_traces(args.url, args.out)
        print(f"fetched traces into {args.out}")
        return

    traces = load_traces(args.traces)
    scores = evaluate_traces(traces)
    write_report(scores, args.out, args.summary)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

