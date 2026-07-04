.PHONY: format
format:
	uv run ruff format .

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: test
test:
	uv run pytest

.PHONY: typecheck
typecheck:
	uv run mypy src

.PHONY: verify
verify:
	uv run ruff check --fix .
	uv run ruff format .
	uv run mypy src
	uv run pytest

.PHONY: ci
ci:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src
	uv run pytest

.PHONY:  preflight
preflight:
	make format
	make verify
	git status
