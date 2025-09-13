# Repository Guidelines

These guidelines help contributors work consistently on http-stream-xml. They reflect the current layout, tooling, and CI in this repo.

## Project Structure & Module Organization
- `src/http_stream_xml/`: Library code (`xml_stream.py`, `socket_stream.py`, `entrez.py`, `version.py`).
- `tests/`: Pytest suite (`test_*.py`).
- `docs/`: Sphinx documentation.
- `scripts/`: Helper scripts (build, test, upload, etc.).
- Root files: `tasks.py` (Invoke tasks), `setup.py`, `requirements*.txt`, `.pre-commit-config.yaml`.

## Build, Test, and Development Commands
- `pipx install invoke` then `inv --list`: Discover tasks.
- `inv test`: Run tests excluding `slow` marked tests.
- `inv test_full`: Run full test suite.
- `./scripts/test.sh -k substring`: Run tests via coverage with a filter.
- `inv pre`: Run lint, format, and type checks (pre-commit).
- `inv docs`: Build Sphinx docs to `docs_build`.
- Packaging: `./scripts/build.sh` (wheel) and `./scripts/upload.sh` (twine upload).

## Coding Style & Naming Conventions
- Python 3.11+; use type hints where practical (mypy runs in pre-commit).
- Indentation: 4 spaces; keep lines ≤99–100 chars.
- Lint/format: Ruff (including ruff-format) enforces style; run `inv pre` locally.
- Naming: `snake_case` for modules/functions, `PascalCase` for classes, constants `UPPER_SNAKE_CASE`.

## Testing Guidelines
- Framework: Pytest with coverage; tests live in `tests/` as `test_*.py`.
- Markers: Use `@pytest.mark.slow` for long-running tests (excluded by `inv test`).
- Run: `inv test` (fast), `inv test_full` (all). View coverage in CLI report from `scripts/test.sh`.

## Commit & Pull Request Guidelines
- Commits: Short, imperative subject; explain “what/why”. Reference issues (e.g., `#6`) when applicable.
- PRs: Include a clear description, linked issues, before/after notes for behavior changes, and test updates. Ensure CI is green and `inv pre` passes locally.

## Security & Release Notes
- Do not commit secrets. Publishing uses local credentials (see `.pypirc`); verify with `./scripts/install_local.sh` before uploading.
- Versioning is automated via scripts/tasks; coordinate version bumps with maintainers when preparing a release.
