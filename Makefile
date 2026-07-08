PYTHON ?= python

.PHONY: help bootstrap lint format format-check test coverage validate-config run-api precommit phase1-check ci-local

help:
	@echo "Available commands:"
	@echo "  make bootstrap        Install project and development dependencies"
	@echo "  make lint             Run ruff linting"
	@echo "  make format           Format Python files with ruff"
	@echo "  make format-check     Check Python formatting without rewriting files"
	@echo "  make test             Run unit tests"
	@echo "  make coverage         Run tests with coverage report"
	@echo "  make validate-config  Validate mock robot YAML configuration"
	@echo "  make run-api          Start the mock robot FastAPI app"
	@echo "  make precommit        Run pre-commit hooks against all files"
	@echo "  make phase1-check     Run local Phase 1 quality checks"
	@echo "  make ci-local         Run local CI-equivalent checks"

bootstrap:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

format-check:
	$(PYTHON) -m ruff format --check .

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov=robot_mock --cov-report=term-missing --cov-report=html --cov-fail-under=70

validate-config:
	$(PYTHON) scripts/validate_config.py

run-api:
	$(PYTHON) -m uvicorn robot_mock.app.api:app --reload --host 127.0.0.1 --port 8000

precommit:
	$(PYTHON) -m pre_commit run --all-files

phase1-check: lint test validate-config

ci-local: lint format-check coverage validate-config
