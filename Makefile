.PHONY: install test lint clean run

# Default Python interpreter
PYTHON = python3

# Install dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt

# Run tests
test:
	$(PYTHON) -m pytest tests/

# Run tests with coverage
test-cov:
	$(PYTHON) -m pytest --cov=src tests/

# Run type checking
lint:
	$(PYTHON) -m mypy src/

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the application (requires API key)
run:
	@echo "Usage: make run API_KEY=your_api_key_here"
	@if [ -z "$(API_KEY)" ]; then \
		echo "Error: API_KEY is required. Use 'make run API_KEY=your_api_key_here'"; \
		exit 1; \
	fi
	$(PYTHON) main.py --api-key $(API_KEY)
