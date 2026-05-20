# Agent Trace Evaluator

This is an internal Translucid challenge template, not a generated candidate repository.

It creates AI-agent evaluation challenges where a candidate must score the whole agent run: trace parsing, tool path correctness, evidence use, loop behavior, escalation decisions, latency, cost, and final machine-readable reporting.

The generated candidate repo is intentionally flawed. It overweights final answer text and misses trajectory-level failures. Public validation should fail for known expected markers until the candidate fixes the evaluator.

## Local Simulator

The candidate repo includes a Docker-backed fake trace API plus Jaeger:

```txt
fake trace API -> deterministic span emitter -> Jaeger UI -> trace parser -> trajectory scorer -> report writer
```

No external credentials, model providers, LangSmith, OpenAI API keys, or customer traces are required.

## Template Commands

```bash
make validate-solution
make validate-candidate-main-expected-failure
make render
make scan-safety
make validate-docker-integration
make validate
```

`validate-solution` proves the reference implementation passes public and hidden tests.

`validate-candidate-main-expected-failure` proves the starter fails public unit validation for expected markers.

`validate-docker-integration` starts the fake trace API and confirms the starter fails the integration gate for expected reasons.

`render` creates `generated/main` and `generated/solution`.

`scan-safety` verifies the rendered candidate main does not leak solution/evaluator/internal material.

## Expected Starter Failures

- `wrong_tool_path_not_penalized`
- `missing_evidence_not_penalized`
- `loop_not_detected`
- `escalation_not_penalized`
- `unstable_report_output`

## For Challenge Creation Agents

Do not infer how to use this template from README prose.

Read `translucid-template.json`.

Normal use:

```bash
make render
make scan-safety
make validate-solution
make validate-candidate-main-expected-failure
make validate-docker-integration
```

Use:

- `generated/main` as candidate-facing main branch
- `generated/solution` as private solution/evaluator branch

Do not manually copy `candidate/` to root.
Do not manually restructure `solution/`.
Do not edit hidden tests or evaluator imports unless a validation command fails and the exact blocker is recorded.

