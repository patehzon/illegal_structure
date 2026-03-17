.PHONY: bootstrap check test run-backend run-frontend

PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

bootstrap:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r backend/requirements.txt
	cd frontend && npm install

check:
	$(PYTHON) -m compileall backend rules etl

test:
	$(PYTHON) -m unittest discover -s backend/tests -p 'test_*.py'

run-backend:
	$(PYTHON) -m uvicorn backend.app.main:app --host 0.0.0.0 --port $${BACKEND_PORT:-8000} --reload

run-frontend:
	cd frontend && npm run dev -- --host 0.0.0.0 --port $${FRONTEND_PORT:-5173}
