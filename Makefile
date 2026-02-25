.PHONY: install lint format typecheck test test-unit test-integration run mermaid docker-build docker-run clean

install:
	uv sync

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

typecheck:
	uv run mypy src/

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit -v

test-integration:
	uv run pytest tests/integration -v

run:
	uv run python -m reflection_agent

mermaid:
	uv run python -m reflection_agent --mermaid

docker-build:
	docker build -t reflection-agent .

docker-run: docker-build
	docker run --env-file .env reflection-agent

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .ruff_cache .mypy_cache .pytest_cache htmlcov .coverage
