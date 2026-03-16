.PHONY: bootstrap check test run-backend run-frontend

bootstrap:
	@echo "Scaffold bootstrap complete. Install backend/frontend dependencies as needed."

check:
	python3 -m compileall backend rules etl

test:
	python3 -m unittest discover -s backend/tests -p 'test_*.py'

run-backend:
	uvicorn backend.app.main:app --host 0.0.0.0 --port $${BACKEND_PORT:-8000} --reload

run-frontend:
	cd frontend && npm run dev -- --host 0.0.0.0 --port $${FRONTEND_PORT:-5173}
