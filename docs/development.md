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
sphinx-build -W -b html docs docs/_build/html
open docs/_build/html/index.html
```

CI runs the same `sphinx-build -W` command on every push (see the `check` job).

Live reload (optional):

```bash
pip install sphinx-autobuild
sphinx-autobuild docs docs/_build/html --open-browser
```

## Continuous integration

GitHub Actions (see [`.github/workflows/ci.yml`](https://github.com/eddiethedean/csvdir/blob/main/.github/workflows/ci.yml)):

| Job | Steps |
|-----|-------|
| `check` | ruff, mypy |
| `test` | pytest on Python 3.10–3.13 |

## Documentation hosting

Docs are built on [Read the Docs](https://csvdir.readthedocs.io/) from `.readthedocs.yaml` using Sphinx, the [Furo](https://pradyunsg.me/furo/) theme, and [MyST](https://myst-parser.readthedocs.io/) Markdown — same stack as the [StreamTree docs](https://streamtree.readthedocs.io/en/latest/).

Open a pull request to trigger an RTD preview build when configured in the project dashboard.

## Release checklist

1. Update version in `csvdir/__init__.py` and `pyproject.toml`
2. Update [CHANGELOG](CHANGELOG.md)
3. Run tests, ruff, mypy, and `sphinx-build -W`
4. Tag and publish to PyPI
5. Confirm RTD builds `latest`

## Repository README

Contributing conventions, badges, and quick usage live in the canonical [README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md).
