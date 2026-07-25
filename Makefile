.PHONY: setup lint validate security clean pre-commit

setup:
	@echo "Setting up Python environment via uv..."
	uv sync
	uv pip install pre-commit ruff bandit

pre-commit:
	@echo "Installing pre-commit hooks..."
	uv run pre-commit install

lint:
	@echo "Running ruff linter..."
	uv run ruff check src/

validate:
	@echo "Validating JSON schemas..."
	uv run python -m src.validate_schemas

security:
	@echo "Running bandit security checks..."
	uv run bandit -r src/ -c pyproject.toml

clean:
	rm -rf .venv
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
