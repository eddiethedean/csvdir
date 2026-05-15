# csvdir

[![CI](https://github.com/eddiethedean/csvdir/actions/workflows/ci.yml/badge.svg)](https://github.com/eddiethedean/csvdir/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/csvdir/badge/?version=latest)](https://csvdir.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/csvdir.svg)](https://pypi.org/project/csvdir/)
[![Python](https://img.shields.io/pypi/pyversions/csvdir.svg)](https://pypi.org/project/csvdir/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/eddiethedean/csvdir/blob/main/LICENSE)

Read every CSV in a directory as one stream of rows — no manual file loops, no header surprises.

**csvdir** is a small, dependency-free library for treating a folder of CSV files like a single dataset. **Documentation:** [readthedocs](https://csvdir.readthedocs.io/en/latest/) · [docs source](https://github.com/eddiethedean/csvdir/tree/main/docs)

## Features

- [**Directory-wide iteration**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/iteration.md) — stream rows from all matching files in sorted order
- [**Header validation**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/headers.md) — lock to a schema, auto-adopt the first file’s headers, or skip mismatches
- [**Chunked reading**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/chunking.md) — `chunksize` for memory-friendly batches
- [**Dialect & encoding**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/encodings.md) — `delimiter`, `quotechar`, `encoding`, BOM handling, and more
- [**File discovery**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/discovery.md) — recursive scan, extensions, hidden files
- [**Column helpers**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/columns.md) — single-column or multi-column views with file labels
- [**Pandas integration**](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/pandas.md) — `CsvDirFile` for `pandas.read_csv`
- **Typed** — ships with [`py.typed`](https://github.com/eddiethedean/csvdir/blob/main/csvdir/py.typed) ([API reference](https://github.com/eddiethedean/csvdir/blob/main/docs/reference/index.md))

## Installation

```bash
pip install csvdir
```

Requires **Python 3.10+**. No runtime dependencies. See the [installation guide](https://github.com/eddiethedean/csvdir/blob/main/docs/installation.md) for editable installs and optional extras.

## Quick start

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    print(row)
# {'id': '1', 'name': 'Alice', 'age': '30'}
# {'id': '2', 'name': 'Bob', 'age': '25'}
```

More examples: [Quickstart](https://github.com/eddiethedean/csvdir/blob/main/docs/quickstart.md)

## Usage

| Topic | Guide |
|-------|--------|
| Row iteration, `with_names()`, `with_paths()` | [Iteration](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/iteration.md) |
| `strict_headers`, `expected_headers`, `on_mismatch` | [Headers](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/headers.md) |
| `chunksize`, `read_dir_chunks` | [Chunking](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/chunking.md) |
| `iter_column`, `select_columns` | [Columns](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/columns.md) |
| `recurse`, `extension`, hidden files | [Discovery](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/discovery.md) |
| `CsvDirFile` + pandas | [Pandas](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/pandas.md) |
| Encodings, BOM, quote sniffing | [Encodings](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/encodings.md) |

### Row iteration

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    ...

for name, row in read_dir("/data/csvs").with_names():
    ...

for path, row in read_dir("/data/csvs").with_paths():
    ...
```

Details: [Iteration guide](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/iteration.md)

### Header validation

```python
for row in read_dir("/data/csvs", strict_headers=True, on_mismatch="skip"):
    ...

for row in read_dir(
    "/data/csvs",
    expected_headers=["id", "name", "age"],
):
    ...
```

Details: [Headers guide](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/headers.md)

### Chunked iteration

```python
for chunk in read_dir("/data/csvs", chunksize=1000):
    process(chunk)  # list[dict[str, str]]
```

Details: [Chunking guide](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/chunking.md)

### Column selection

```python
r = read_dir("/data/csvs")

for name, value in r.with_names().iter_column("name"):
    ...

for name, row in r.with_names().select_columns(["name", "age"]):
    ...
```

Details: [Columns guide](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/columns.md)

### Pandas

```python
import pandas as pd
from csvdir import CsvDirFile

df = pd.read_csv(CsvDirFile("/data/csvs", on_mismatch="skip"))
```

Details: [Pandas guide](https://github.com/eddiethedean/csvdir/blob/main/docs/guide/pandas.md)

## Configuration & API

- [**Full option reference**](https://github.com/eddiethedean/csvdir/blob/main/docs/reference/options.md) — every `read_dir` / `CsvDirFile` parameter
- [**API reference**](https://github.com/eddiethedean/csvdir/blob/main/docs/reference/index.md) — autodoc for all public types and functions
- [**Changelog**](https://github.com/eddiethedean/csvdir/blob/main/docs/changelog.md)

## Development

```bash
git clone https://github.com/eddiethedean/csvdir.git
cd csvdir
pip install -e ".[dev,docs]"

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
ruff check csvdir tests && ruff format csvdir tests
mypy
sphinx-build -b html docs docs/_build/html
```

See the [development guide](https://github.com/eddiethedean/csvdir/blob/main/docs/development.md). CI: [`.github/workflows/ci.yml`](https://github.com/eddiethedean/csvdir/blob/main/.github/workflows/ci.yml) (ruff, mypy, pytest on Python 3.10–3.13).

## License

MIT © 2025–2026 — see [LICENSE](https://github.com/eddiethedean/csvdir/blob/main/LICENSE). Release notes: [changelog](https://github.com/eddiethedean/csvdir/blob/main/docs/changelog.md).
