# Reflection Agent

Production-grade **LangGraph** agent that iteratively refines content through a **generate → reflect → generate** loop.
Built with professional software engineering practices: validated configuration, structured logging, comprehensive tests, CI/CD, and container-ready deployment.

## Architecture

```
src/reflection_agent/
├── __init__.py              # Package metadata
├── __main__.py              # python -m reflection_agent
├── cli.py                   # CLI entry-point (argparse)
├── logging.py               # Structured logging (structlog)
├── config/
│   ├── settings.py          # Pydantic BaseSettings — validated config
│   └── llm_strategies.py    # Strategy pattern for LLM providers
├── graph/
│   ├── state.py             # TypedDict state + node name enum
│   ├── prompts.py           # Prompt templates (easy versioning/A-B testing)
│   ├── chains.py            # LCEL chain factories (prompt | llm)
│   ├── nodes.py             # Node functions (generate, reflect)
│   └── builder.py           # Graph wiring and compilation
└── exceptions/
    └── base.py              # Domain exception hierarchy
```

### Design Patterns

| Pattern | Where | Why |
|---------|-------|-----|
| **Strategy** | `llm_strategies.py` | Swap LLM providers without touching graph logic |
| **Factory** | `chains.py` | Build chains with injectable LLM (testable) |
| **Singleton** (cached) | `get_settings()` | One validated config instance, cached |
| **Template Method** | `prompts.py` | Isolated prompt templates for easy versioning |

## Quick Start

```bash
# 1. Clone and install
git clone <repo-url> && cd reflection_agent
cp .env.example .env          # Add your API keys
uv sync                       # Install all dependencies

# 2. Run
uv run python -m reflection_agent "Write a viral tweet about AI"
uv run python -m reflection_agent --mermaid   # Print graph diagram

# 3. Or use Make
make run
make mermaid
```

## Development

```bash
make install          # Install dependencies (including dev)
make lint             # Ruff linting
make format           # Auto-format with Ruff
make typecheck        # mypy type checking
make test             # Full test suite with coverage
make test-unit        # Unit tests only
make test-integration # Integration tests only
```

### Pre-commit hooks

```bash
uv run pre-commit install     # One-time setup
uv run pre-commit run --all   # Manual run
```

## Configuration

All settings via environment variables (or `.env` file). Validated at startup by Pydantic:

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PROVIDER` | `openai` | `openai` or `anthropic` |
| `REFLECTION_MAX_MESSAGES` | `6` | Loop iteration limit (min: 2) |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | Model identifier |
| `OPENAI_TEMPERATURE` | `0.7` | Sampling temperature (0.0–2.0) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `ENVIRONMENT` | `development` | `development` (pretty logs) or `production` (JSON logs) |

## Docker

```bash
make docker-build     # Build image
make docker-run       # Build and run with .env

# Or manually
docker compose up --build
```

## CI/CD

GitHub Actions pipeline (`.github/workflows/ci.yml`) runs on every push/PR to `main`:
- Lint (ruff)
- Format check
- Type check (mypy)
- Unit tests
- Integration tests
- Python 3.12 + 3.13 matrix

## Testing

```bash
make test              # Full suite with coverage report
make test-unit         # Fast unit tests only
```

Tests use `FakeLLM` stubs — no API keys or network needed for the test suite.
