# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

Slide Gen is an open-source Python package that generates beautiful
background images for presentation slides using pluggable AI providers. It
supports OpenAI, Google Gemini, Ollama, and LM Studio with a flexible
architecture for easy extension.

## Key Commands

### Development Setup

```bash
# Full development setup (recommended)
just setup

# Individual setup steps
just install        # Install with uv in virtual environment
just setup-examples # Create example files
just config-template # Generate config template

# Manual uv setup
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"
```

### Code Quality and Testing

```bash
# Format and lint code
just format         # black + isort formatting
just lint          # flake8 + mypy linting
just lint-fix      # auto-fix formatting issues

# Run tests
just test          # all tests with pytest
just test-fast     # skip slow/integration tests
just test-cov      # with coverage reporting

# Run single test file/function
uv run pytest tests/test_specific.py
uv run pytest tests/test_file.py::test_function
```

### Usage Examples

```bash
# Generate from slide titles
just example-titles
slide-gen --titles "Modern Architecture" "Cloud Computing"

# Generate from files
just example-file
slide-gen --file examples/slides.md

# Health checks and provider info
just health-check
just providers
```

### Building and Publishing

```bash
just build         # build package with python -m build
just publish-test  # publish to test PyPI
just publish       # publish to PyPI
just clean         # cleanup build artifacts
```

### Configuration Management

```bash
# Create .env file from template (recommended)
just env-template

# Create JSON config template (advanced)
just config-template

# Edit .env file with your API keys
# OPENAI_API_KEY=your-key
# GEMINI_API_KEY=your-key
# OLLAMA_BASE_URL=http://localhost:11434
# LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

## Architecture

### Core Components

- **`src/slide_gen/providers/`**: Pluggable AI provider
  implementations

  - `base.py`: Abstract provider interface with `AIProvider`, `PromptRequest`,
    `ImageRequest`, `AIResponse`
  - `openai_provider.py`: OpenAI GPT-4 and DALL-E integration
  - `gemini_provider.py`: Google Gemini and Imagen integration
  - `ollama_provider.py`: Local Ollama models (prompt-only)
  - `lmstudio_provider.py`: LM Studio local server (prompt-only)

- **`src/slide_gen/processors/`**: Content processing and
  orchestration

  - `slide_processor.py`: Handles JSON, Markdown, and text input formats
  - `image_generator.py`: Orchestrates prompt generation and image creation

- **`src/slide_gen/utils/`**: Configuration and utilities

  - `config_loader.py`: Provider factory and configuration management
  - `file_utils.py`: File operations, image saving, filename sanitization

- **`src/slide_gen/cli.py`**: Command-line interface with async
  support

### Key Design Patterns

- **Abstract Factory**: `ConfigLoader` creates providers based on configuration
- **Strategy Pattern**: Pluggable AI providers with common interface
- **Async/Await**: All AI operations are asynchronous with concurrent processing
- **Session Management**: Timestamped output directories with metadata

### Input Processing

Supports multiple formats:

- **JSON**: Structured slide data with titles, content, and bullet points
- **Markdown**: Headers become slide titles, content extracted automatically
- **Plain Text**: Line-separated slide titles or section-separated slides
- **CLI**: Direct slide title arguments

### Provider Capabilities

- **OpenAI**: Full support (prompts + images via GPT-4 + DALL-E)
- **Gemini**: Full support (prompts + images via Gemini + Imagen)
- **Ollama**: Prompt generation only (local models)
- **LM Studio**: Prompt generation only (local OpenAI-compatible API)

### Configuration System

- Environment variables take precedence over config files
- JSON configuration files with provider-specific settings
- Factory pattern for provider instantiation
- Health check capabilities for all providers

## Development Notes

### Adding New Providers

1. Inherit from `AIProvider` in `providers/base.py`
2. Implement required abstract methods: `generate_prompt()`, `generate_image()`,
   `supports_image_generation()`, `supports_prompt_generation()`
3. Add provider class to `config_loader.py` PROVIDER_CLASSES dictionary
4. Update CLI choices in `cli.py` parser arguments
5. Add environment variable handling in `ConfigLoader._load_from_env()`

### Async Architecture

- All AI operations use async/await for concurrent processing
- Uses `aiohttp.ClientSession` for HTTP clients with proper timeout handling
- Semaphore-based concurrency limiting via `asyncio.Semaphore` in
  `ImageGenerator`
- Exception handling with graceful degradation and detailed error responses
- Request/Response dataclasses: `PromptRequest`, `ImageRequest`, `AIResponse`

### Configuration System

- `.env` file for API keys and settings (loaded via python-dotenv)
- Environment variables take precedence over JSON config files
- `ConfigLoader` acts as factory for provider instantiation
- Provider-specific configuration with fallback defaults
- Health check capabilities for all providers via `health_check()` method
- Configuration validation and missing key handling
- `.env.example` template for easy setup

### Error Handling and Resilience

- Comprehensive error responses with provider-specific error messages
- Timeout handling with configurable timeouts per provider
- Health checks for provider availability before generation
- Graceful handling of missing API keys, network failures, connection errors
- Session-level error tracking and reporting

### Output Management

- Session-based timestamped directories (YYYYMMDD_HHMMSS format)
- JSON metadata for each generation with full request/response details
- Markdown reports with embedded images and generation summaries
- PNG image format with RGB conversion for transparency handling
- Filename sanitization for cross-platform compatibility

### CLI Architecture

- Async CLI with `asyncio.run()` entry point
- Mutually exclusive input groups (file vs titles)
- Argument validation and provider choice constraints
- Rich help system with examples and health checks
- Configuration template generation utilities

## Testing Strategy

- Async test support with pytest-asyncio auto mode
- Integration tests marked with `@pytest.mark.integration`
- Slow tests marked with `@pytest.mark.slow` (skip with `-m "not slow"`)
- Coverage reporting with HTML, XML, and terminal output
- Provider health checks as smoke tests for integration testing
- Test configuration via pyproject.toml with strict settings
