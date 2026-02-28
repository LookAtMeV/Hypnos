.PHONY: sync format lint type test run check

sync:
	uv sync

format:
	uv run ruff format .

lint:
	uv run ruff check .

type:
	uv run mypy src

test:
	uv run pytest -q

check: format lint type test

run:
	uv run uvicorn hypnos.api.app:app --reload --host 0.0.0.0 --port 8000
