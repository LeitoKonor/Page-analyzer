install:
	poetry install
	
dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

DB_NAME=pageanalyzer
DB_USER=leitokonor

db-build:
	db-drop db-create schema-load

db-drop:
	dropdb $(DB_NAME)

db-create:
	createdb $(DB_NAME)

schema-load:
	psql $(DB_NAME) < database.sql

db-reset:
	dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

connect:
	psql -d $(DB_NAME)


lint:
	poetry run flake8 page_analyzer

