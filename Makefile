# Simple helper tasks
.PHONY: setup lint test format evaluate

PYTHON=python
VENV?=.venv

setup:
	@echo "[setup] Creating venv (if missing) and installing week1 deps"
	@if [ ! -d $(VENV) ]; then $(PYTHON) -m venv $(VENV); fi
	@. $(VENV)/bin/activate; pip install -r solutions/week1_prompt_engineering/requirements.txt || true

format:
	@. $(VENV)/bin/activate; ruff format . || echo "Ruff not installed"

lint:
	@. $(VENV)/bin/activate; ruff check . || echo "Ruff not installed"

test:
	@. $(VENV)/bin/activate; pytest -q || echo "Tests failed"

evaluate:
	@echo "Placeholder for evaluation script (to be added)."
