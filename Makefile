VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
SRC_PATH := src

.PHONY: help venv install test clean build sdist wheel run-solve run-week-span run-nth run-windows run-csv run-tz

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@printf "  \033[36m%-15s\033[0m %s\n" "help" "Show this help message"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| grep -v '^help:' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtualenv in .venv
	python3 -m venv $(VENV)

install: venv ## Install package (editable) + dev deps
	$(PIP) install -U pip
	$(PIP) install -e ".[dev]"

test: ## Run tests (pytest)
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -m pytest

build: sdist wheel ## Build source and wheel distributions

sdist: ## Build source distribution
	$(PYTHON) -m build --sdist

wheel: ## Build wheel distribution
	$(PYTHON) -m build --wheel

run-solve: ## Run ISO week listing CLI (usage: make run-solve YEAR=2026)
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -c "from calendar_smith.cli import solve_weeks; solve_weeks()" -- $(YEAR)

run-week-span: ## Run ISO week span CLI (usage: make run-week-span ISO_YEAR=2020 ISO_WEEK=53)
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -c "from calendar_smith.cli import solve_week_span; solve_week_span()" -- $(ISO_YEAR) $(ISO_WEEK)

run-nth: ## Run nth-week CLI
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -c "from calendar_smith.cli import determine_nth_week; determine_nth_week()"

run-windows: ## Run date windows CLI (usage: make run-windows START_DATE=2026-03-17 WINDOW_SIZE=7 REPEATS=4)
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -c "from calendar_smith.cli import generate_windows; generate_windows()" -- $(START_DATE) $(WINDOW_SIZE) $(REPEATS)

run-csv: ## Run CSV fiscal-year CLI (usage: make run-csv INPUT=records.csv OUTPUT=out.csv)
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -c "from calendar_smith.cli import process_csv; process_csv()" -- $(INPUT) $(OUTPUT)

run-tz: ## Run timezone conversion CLI (usage: make run-tz DT_ISO="2026-03-20T10:00:00+09:00" TARGET_TZ="America/New_York")
	PYTHONPATH=$(SRC_PATH) $(PYTHON) -c "from calendar_smith.cli import convert_timezone; convert_timezone()" -- $(DT_ISO) $(TARGET_TZ)

clean: ## Remove build artifacts and Python cache files
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -not -path "*/.venv/*" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -not -path "*/.venv/*" -exec rm -rf {} +
	@rm -rf dist/ build/ src/*.egg-info/ .coverage htmlcov/
	@echo "Cleanup complete."