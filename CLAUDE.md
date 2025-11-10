# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

http-stream-xml is a Python library for parsing XML from HTTP responses on-the-fly by chunks, without needing to load the entire document. The main use case is working with NCBI (PubMed) Entrez API responses.

## Core Architecture

### Main Components

- `src/http_stream_xml/xml_stream.py` - Core XML streaming parser using SAX
  - `XmlStreamExtractor` - Main class that feeds XML chunks to parser
  - `StreamHandler` - SAX content handler that collects specified tags
  - `ExtractionCompleted` - Exception raised when all required tags are found

- `src/http_stream_xml/entrez.py` - NCBI Entrez API integration
  - `Genes` - Main class for fetching gene information from NCBI
  - `GeneFields` - Constants for gene field names in XML responses
  - Implements caching, retry logic, and partial download optimization

- `src/http_stream_xml/socket_stream.py` - Socket-based streaming functionality
- `src/http_stream_xml/examples/` - Usage examples for different scenarios

### Key Design Patterns

- Uses SAX parser for memory-efficient XML processing
- Implements early termination when all required tags are found
- Built-in retry mechanisms for unreliable network connections
- Caching layer for API responses
- Stream processing with configurable timeouts and byte limits

## Development Commands

### Environment Setup
```bash
# Set up or activate development environment
source ./activate.sh
```

**IMPORTANT**: Always activate the virtual environment before running any commands. Use `source ./activate.sh` before each command.

### Testing
```bash
# Run fast tests (exclude slow tests)
source ./activate.sh && inv test
# Or directly: source ./activate.sh && ./scripts/test.sh -m 'not slow'

# Run all tests including slow ones
source ./activate.sh && inv test-full
# Or directly: source ./activate.sh && ./scripts/test.sh

# Run specific test pattern
source ./activate.sh && ./scripts/test.sh -k "pattern_or_substring"

# Test with coverage (built into test scripts)
source ./activate.sh && coverage run -m pytest
source ./activate.sh && coverage report --omit='tests/*'
```

### Code Quality
```bash
# Run pre-commit checks (linting, formatting, type checking)
source ./activate.sh && inv pre
# Or directly: source ./activate.sh && pre-commit run --verbose --all-files
```

**IMPORTANT**: Always use `pre-commit run --all-files` for code quality checks. Never run ruff or mypy directly.

### Building and Dependencies
```bash
# Build package
source ./activate.sh && ./scripts/build.sh
# Or directly: source ./activate.sh && python setup.py bdist_wheel

# Compile requirements
source ./activate.sh && inv compile-requirements
# Or directly: source ./activate.sh && uv pip compile requirements.in --output-file=requirements.txt --upgrade

# Install/upgrade dependencies
source ./activate.sh && inv reqs
```

### Documentation
```bash
# Build documentation
inv docs
# Or directly: sphinx-build docs docs_build

# Check documentation links
inv docs-check
```

## Project Configuration

- **Python version**: Requires Python 3.11+
- **Dependencies**: Managed via requirements.in/requirements.txt with uv
- **Linting**: ruff with strict configuration (line length 100, extensive rule set)
- **Type checking**: mypy with strict settings
- **Testing**: pytest with coverage reporting
- **Build system**: Traditional setup.py (not pyproject.toml)

## Key Files and Structure

- `src/http_stream_xml/` - Main package source
- `tests/` - Test suite with pytest
- `scripts/` - Shell scripts for common development tasks
- `tasks.py` - invoke task definitions for development commands
- `requirements.in` / `requirements.dev.in` - Dependency specifications
- `.pre-commit-config.yaml` - Code quality automation

## Testing Strategy

Tests are organized to support both fast and comprehensive testing:
- Fast tests run by default (exclude tests marked as 'slow')
- Full test suite includes integration tests with external APIs
- Coverage reporting is integrated into test runs
- Tests exclude the `tests/` directory from linting to allow more flexible test code
