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

1. Update version in `csvdir/__init__.py` and `pyproject.toml`
2. Update [CHANGELOG](CHANGELOG.md)
3. Run tests, ruff, mypy, and `python -m mkdocs build --strict`
4. Tag and publish to PyPI
5. Confirm RTD builds `latest`

## Repository README

Contributing conventions, badges, and quick usage live in the **canonical [README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md)**.
