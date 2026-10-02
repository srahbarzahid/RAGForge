.PHONY: dev-api dev-web lint format format-check test build

dev-api:
	cd backend && python -m uvicorn app.main:app --reload

dev-web:
	cd frontend && npm run dev

lint:
	cd backend && python -m ruff check .
	cd frontend && npm run lint

format:
	cd backend && python -m ruff format .
	cd frontend && npm run format

format-check:
	cd backend && python -m ruff format --check .
	cd frontend && npm run format:check

test:
	cd backend && python -m pytest

build:
	cd frontend && npm run build
