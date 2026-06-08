.PHONY: run view-types format test migrate

run dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

format:
	poetry run black .

view-types:
	poetry run mypy .

test:
	poetry run pytest

start pipeline: format view-types test