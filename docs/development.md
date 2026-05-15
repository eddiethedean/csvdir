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
3. Push a **Git tag** `vX.Y.Z` that matches `pyproject.toml` (e.g. `git tag v0.9.0 && git push origin v0.9.0`). Pushing the tag runs **[Release](https://github.com/eddiethedean/csvdir/actions)** (`.github/workflows/release.yml`): same checks as CI, tag/version check, then PyPI upload via secret **`PYPI_API_TOKEN`** (*Settings → Secrets and variables → Actions*).
4. Optionally create a **GitHub Release** from that tag for release notes (the Release workflow is **not** tied to the Release UI — only the tag push matters).
5. Confirm Read the Docs builds **`latest`** (and any versioned doc build you use).

To publish manually instead: `python -m build` then `twine upload dist/*`.

## Repository README

Contributing conventions, badges, and quick usage live in the **canonical [README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md)**.
