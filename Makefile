install:
	poetry install
	
dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

db-build:
	db-drop db-create schema-load

db-drop:
	dropdb pageanalyzer

db-create:
	createdb pageanalyzer

schema-load:
	psql pageanalyzer < database.sql

test:
	poetry run flake8 page_analyzer

