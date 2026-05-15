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
pip install -e ".[docs]"
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html
```

Live reload (optional):

```bash
pip install sphinx-autobuild
sphinx-autobuild docs docs/_build/html --open-browser
```

## Continuous integration

GitHub Actions runs on Python 3.10–3.13:

| Job | Steps |
|-----|-------|
| `check` | ruff, mypy |
| `test` | pytest matrix |

## Documentation hosting

Docs are built on [Read the Docs](https://csvdir.readthedocs.io/) from `.readthedocs.yaml` using Sphinx, the [Furo](https://pradyunsg.me/furo/) theme, and [MyST](https://myst-parser.readthedocs.io/) Markdown.

To preview RTD builds, open a pull request — RTD creates a preview URL automatically when configured in the project dashboard.

## Release checklist

1. Update version in `csvdir/__init__.py` and `pyproject.toml`
2. Update `docs/changelog.md`
3. Run tests, ruff, mypy, and `sphinx-build` with `-W` (warnings as errors)
4. Tag and publish to PyPI
5. Confirm RTD builds the `latest` docs
