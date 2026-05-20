# Template Progress

| # | Template | Coverage | Local services | Status | Validation |
| -: | --- | --- | --- | --- | --- |
| 1 | async-webhook-ledger | backend reliability, webhooks, idempotency | Postgres, LocalStack, WireMock, MailHog | golden-template-candidate | remote CI previously accepted |
| 2 | rag-retrieval-quality-lab | AI backend, retrieval, citations | Qdrant, Postgres, MinIO, fake embeddings | golden-template-candidate | remote CI previously accepted |
| 3 | gpu-fault-correlation-drain-scheduler | ML infra, telemetry, scheduling | Prometheus/fake telemetry/LocalStack-style simulator | golden-template-candidate | local/remote validation tracked in repo |
| 4 | streaming-chat-budget-tools | full-stack AI, streaming, tools, budget | fake streaming model/tool simulator | golden-template-candidate | remote CI accepted |
| 5 | agent-trace-evaluator | AI evals, agent trajectory scoring | fake trace API, Jaeger | golden | explicit Jaeger post assertion added; local/remote validation required |
## Machine-Readable Contract Migration

- machine_readable_manifest: present
- root_make_aliases: present
- render_context_support: present
- check_render_contract: present
- scan_safety_uses_manifest: present
- remote_ci_manifest_validation: passed

