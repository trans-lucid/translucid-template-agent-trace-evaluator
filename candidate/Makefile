PYTHON ?= python3

.PHONY: setup dev logs seed generate-traces test test-unit test-integration eval run clean

setup:
	$(PYTHON) -m pip install -e .[test]

dev:
	docker compose up -d

logs:
	docker compose logs -f

seed: setup
	$(PYTHON) -m src.cli seed --out traces/public_runs.jsonl

generate-traces: setup
	$(PYTHON) -m src.cli fetch --url http://localhost:8089/traces/public --out traces/public_runs.jsonl

test: setup
	$(PYTHON) -m pytest tests/public

test-unit: setup
	$(PYTHON) -m pytest tests/public/test_public.py

test-integration: setup
	$(PYTHON) -m pytest tests/public/test_integration_trace_api.py

eval: setup
	$(PYTHON) -m src.cli evaluate --traces traces/public_runs.jsonl --out results/evaluation_report.json --summary results/summary.md

run:
	$(MAKE) eval

clean:
	docker compose down -v
