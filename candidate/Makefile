.PHONY: dev logs seed generate-traces test test-unit test-integration eval run clean

dev:
	docker compose up -d

logs:
	docker compose logs -f

seed:
	python -m src.cli seed --out traces/public_runs.jsonl

generate-traces:
	python -m src.cli fetch --url http://localhost:8089/traces/public --out traces/public_runs.jsonl

test:
	python -m pytest tests/public

test-unit:
	python -m pytest tests/public/test_public.py

test-integration:
	python -m pytest tests/public/test_integration_trace_api.py

eval:
	python -m src.cli evaluate --traces traces/public_runs.jsonl --out results/evaluation_report.json --summary results/summary.md

run:
	$(MAKE) eval

clean:
	docker compose down -v
