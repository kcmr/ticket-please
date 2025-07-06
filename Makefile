.PHONY: help setup format lint test check clean clean-all install dev-install install-hooks

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	poetry install
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg

install: ## Install the package in development mode
	poetry install

dev-install: ## Install development dependencies
	poetry install --with dev

install-hooks: ## Install pre-commit hooks
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg

format: ## Format code with ruff
	poetry run ruff format src/ tests/

lint: ## Lint code with ruff
	poetry run ruff check --fix src/ tests/

test: ## Run tests with pytest
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=src/cli --cov=src/ai --cov=src/config --cov=src/ticketplease --cov-report=term-missing

check: format lint test ## Run all checks (format, lint, test)

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

clean-all: ## Clean everything (cache, dependencies, build artifacts)
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
