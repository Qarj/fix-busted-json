.DEFAULT_GOAL := help

PYTHON := python
SRC := src
PYTHONPATH := $(SRC)
export PYTHONPATH

# Detect OS for 'open' command (macOS vs Linux)
UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
	OPEN := open
else
	OPEN := xdg-open
endif

.PHONY: help test test-all coverage coverage-report examples lint build install clean publish publish-test

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

test: ## Run the unit test suite
	$(PYTHON) tests/tests.py

test-all: test examples ## Run unit tests and all examples

examples: ## Run every example script (smoke test the public API)
	@for f in examples/*.py; do echo "--- $$f ---"; $(PYTHON) "$$f" || exit 1; done

coverage: ## Run tests under coverage and print a report with missing lines
	$(PYTHON) -m coverage run --source=$(SRC) tests/tests.py
	$(PYTHON) -m coverage report -m

coverage-report: coverage ## Generate the HTML coverage report and open it
	$(PYTHON) -m coverage html
	@echo "Opening coverage report..."
	$(OPEN) htmlcov/index.html

lint: ## Lint the source with flake8 (if installed)
	$(PYTHON) -m flake8 $(SRC) tests

build: clean ## Build the sdist and wheel into dist/
	$(PYTHON) setup.py sdist bdist_wheel

install: ## Install the package in editable mode
	pip install -e .

clean: ## Remove build artifacts and coverage output
	rm -rf dist build htmlcov .coverage
	rm -rf $(SRC)/*.egg-info

publish: build ## Upload the built distribution to PyPI
	$(PYTHON) -m twine upload dist/*

publish-test: build ## Upload the built distribution to TestPyPI
	$(PYTHON) -m twine upload --repository testpypi dist/*
