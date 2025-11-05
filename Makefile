.PHONY: help install test lint format coverage clean

help:
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run all linters (ruff, mypy, bandit)"
	@echo "  make format      - Format code with ruff"
	@echo "  make coverage    - Generate coverage report"
	@echo "  make clean       - Clean up generated files"

install:
	cd backend && pip3 install -r requirements.txt
	cd frontend && npm install

test:
	cd backend && python3 -m pytest --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=70 -v

lint:
	@echo "Running ruff..."
	cd backend && ruff check .
	@echo "Running mypy..."
	cd backend && mypy . --ignore-missing-imports || true
	@echo "Running bandit..."
	cd backend && bandit -r . -ll || true

format:
	cd backend && ruff format .
	cd backend && ruff check --fix .

coverage:
	cd backend && python3 -m pytest --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in backend/htmlcov/index.html"

clean:
	rm -rf backend/__pycache__ backend/**/__pycache__
	rm -rf backend/.pytest_cache backend/htmlcov backend/.coverage
	rm -rf frontend/node_modules frontend/build

