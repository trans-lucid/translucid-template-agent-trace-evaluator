# Agent Trace Evaluator

You are joining an AI-agent startup. The support agent often gives plausible final answers, but its path can still be unsafe: wrong tools, unsupported claims, repeated failed tool loops, confident answers when escalation is required, and latent cost/latency regressions.

Your task is to build an evaluator that scores the whole run, not just the final answer.

## What To Build

- trace parser
- trajectory scorer
- tool correctness checks
- evidence/citation checks
- loop detection
- escalation decision scoring
- final machine-readable report

## Local Simulator

`make dev` starts a local fake trace API and a Jaeger trace UI. The integration test fetches traces through the API, emits deterministic spans into Jaeger, and then runs the evaluator.

No external credentials are required. Do not call live model providers, LangSmith, OpenAI, or hosted tracing services.

## Main Files

- `src/trace_schema.py`
- `src/evaluator.py`
- `src/metrics.py`
- `src/report.py`
- `src/cli.py`

## Commands

```bash
python -m pip install -e .[test]
make dev
make seed
make generate-traces
make test
make test-integration
make eval
make clean
```

## Deliverables

- `results/evaluation_report.json`
- `results/summary.md`
- completed `DEBRIEF.md`

Private tests add harder cases around tool path, evidence, loops, escalation, missing fields, and stable output.
