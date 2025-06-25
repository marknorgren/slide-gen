default:
    @echo "Available tasks:"
    @just --list

# Setup
install:
    @echo "Setting up development environment..."
    uv sync --dev

env-template:
    @echo "Creating .env file from template..."
    @if [ ! -f ".env" ]; then \
        cp .env.example .env; \
        echo ".env file created from .env.example"; \
        echo "Please edit .env and add your API keys"; \
    else \
        echo ".env file already exists"; \
    fi

setup: install env-template
    @echo "Setup complete! Edit .env and add your API keys"

# Testing
test:
    @echo "Running tests..."
    uv run pytest

# Examples
example:
    @echo "Running example..."
    uv run slide-gen --titles "Modern Architecture" "Cloud Computing" "AI Ethics"

example-directory:
    @echo "Running directory example..."
    uv run slide-gen --directory examples/tech-presentation

health-check:
    @echo "Checking provider health..."
    uv run slide-gen --health-check

# Cleanup
clean:
    @echo "Cleaning up..."
    rm -rf build/ dist/ *.egg-info/ .pytest_cache/
    find . -type d -name __pycache__ -delete
    find . -type f -name "*.pyc" -delete