.PHONY: format
format:
	poetry run black .
	poetry run isort .

.PHONY: lint
lint:
	poetry run flake8 .

.PHONY: test
test:
	poetry run pytest

.PHONY: all
all: format lint test