.PHONY: pip-install pre-commit-install install create-db migrate-db upgrade-db downgrade-db lint test format format-check

pip-install:
	pipenv install --dev

pre-commit-install:
	pipenv run pre-commit install

install: pip-install pre-commit-install

create-db:
	createdb --port 5432 --username postgres simple_movie_database
	createdb --port 5432 --username postgres simple_movie_database_test

migrate-db:
	pipenv run migrate_db

upgrade-db:
	pipenv run upgrade_db

downgrade-db:
	pipenv run downgrade_db

lint:
	pipenv run lint

test:
	pipenv run test

check: test lint

format:
	pipenv run format

format-check:
	pipenv run format-check

