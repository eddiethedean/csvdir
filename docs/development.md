# Development

## Setup

```bash
git clone https://github.com/eddiethedean/csvdir.git
cd csvdir
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,docs]"
```

## Run tests

Global pytest plugins can interfere with the suite. Disable autoload when testing locally:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
```

## Lint and type-check

```bash
ruff check csvdir tests
ruff format csvdir tests
mypy
```

## Build documentation locally

```bash
python -m mkdocs build --strict
open site/index.html
```

Live reload (optional):

```bash
pip install mkdocs
python -m mkdocs serve
```

## Continuous integration

GitHub Actions (see [`.github/workflows/ci.yml`](https://github.com/eddiethedean/csvdir/blob/main/.github/workflows/ci.yml)):

| Job | Steps |
|-----|-------|
| `check` | ruff, mypy, `mkdocs build --strict` |
| `test` | pytest on Python 3.10–3.13 |

## Documentation hosting

Docs are built on [Read the Docs](https://csvdir.readthedocs.io/) from `.readthedocs.yml` using **MkDocs Material** and **mkdocstrings** — the same stack as [StreamTree](https://github.com/eddiethedean/streamtree).

## Release checklist

1. Confirm **`csvdir/__init__.py`** `__version__` matches **`pyproject.toml`** `[project] version`.
2. Update **[CHANGELOG](CHANGELOG.md)** for the release: one `## x.y.z` section with user-facing notes.
3. Merge to `main`, then push a **Git tag** `vX.Y.Z` that matches the version (e.g. `v0.9.0` ↔ `0.9.0` in `pyproject.toml`).
4. On GitHub: **Create a new Release** from that tag and **Publish** it. The **[Release workflow](https://github.com/eddiethedean/csvdir/actions)** (`.github/workflows/release.yml`) runs the same checks as CI, verifies the tag matches `pyproject.toml`, builds the sdist/wheel, and uploads to PyPI using the repository secret **`PYPI_API_TOKEN`** (set under *Settings → Secrets and variables → Actions*).
5. Confirm Read the Docs builds **`latest`** (and any versioned doc build you use).

To publish manually instead: `python -m build` then `twine upload dist/*`.

## Repository README

Contributing conventions, badges, and quick usage live in the **canonical [README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md)**.
