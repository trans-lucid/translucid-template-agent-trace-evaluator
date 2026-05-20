.PHONY: install validate-solution validate-candidate-main-expected-failure validate-docker-integration render scan-safety validate-rendered-smoke validate

install:
	python3 -m pip install -e candidate[test]

validate-solution:
	PYTHONPATH=$$(pwd)/solution EVAL_TARGET=$$(pwd)/solution python3 -m pytest candidate/tests/public/test_public.py evaluator/tests_hidden solution/tests

validate-candidate-main-expected-failure:
	bash tools/expect_candidate_failure.sh

validate-docker-integration:
	bash tools/expect_candidate_docker_failure.sh

render:
	python3 tools/render_template.py

scan-safety:
	python3 tools/scan_safety.py generated/main

validate-rendered-smoke:
	bash tools/validate_rendered_smoke.sh

validate:
	$(MAKE) validate-solution
	$(MAKE) validate-candidate-main-expected-failure
	$(MAKE) render
	$(MAKE) scan-safety
	$(MAKE) validate-rendered-smoke
	$(MAKE) validate-docker-integration
