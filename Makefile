.PHONY: help install install-dev fetch-data build-db clean test lint format

help:
	@echo "NBD Database - Makefile Commands"
	@echo ""
	@echo "  make install       - Install package"
	@echo "  make install-dev   - Install with dev dependencies"
	@echo "  make fetch-data    - Fetch all data sources (takes 10-30 min)"
	@echo "  make build-db      - Build SQLite database"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean build files"
	@echo "  make demo          - Run demo"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,build]"

fetch-data:
	@echo "Fetching all data sources..."
	cd scripts && python 1_fetch_names_dataset.py
	cd scripts && python 2_fetch_wikipedia.py
	cd scripts && python 3_fetch_olympics.py
	cd scripts && python 4_fetch_phone_directories.py
	cd scripts && python 5_merge_all_data.py

build-db:
	cd scripts && python 6_create_database.py

test:
	pytest tests/ -v --cov=nbd --cov-report=html

lint:
	flake8 nbd/ tests/ --max-line-length=120
	pylint nbd/

format:
	black nbd/ tests/ scripts/
	isort nbd/ tests/ scripts/

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

demo:
	python examples/demo.py
