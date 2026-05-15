# csvdir

[![CI](https://github.com/eddiethedean/csvdir/actions/workflows/ci.yml/badge.svg)](https://github.com/eddiethedean/csvdir/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/csvdir/badge/?version=latest)](https://csvdir.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/csvdir.svg)](https://pypi.org/project/csvdir/)
[![Python](https://img.shields.io/pypi/pyversions/csvdir.svg)](https://pypi.org/project/csvdir/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/eddiethedean/csvdir/blob/main/LICENSE)

Read every CSV in a directory as one stream of rows — no manual file loops, no header surprises.

**csvdir** is a small, dependency-free library for treating a folder of CSV files like a single dataset. **Documentation:** [csvdir.readthedocs.io](https://csvdir.readthedocs.io/en/latest/) · [docs source on GitHub](https://github.com/eddiethedean/csvdir/tree/main/docs)

## Features

- [**Directory-wide iteration**](https://csvdir.readthedocs.io/en/latest/guide/iteration.html) — stream rows from all matching files in sorted order
- [**Header validation**](https://csvdir.readthedocs.io/en/latest/guide/headers.html) — lock to a schema, auto-adopt the first file’s headers, or skip mismatches
- [**Chunked reading**](https://csvdir.readthedocs.io/en/latest/guide/chunking.html) — `chunksize` for memory-friendly batches
- [**Dialect & encoding**](https://csvdir.readthedocs.io/en/latest/guide/encodings.html) — `delimiter`, `quotechar`, `encoding`, BOM handling, and more
- [**File discovery**](https://csvdir.readthedocs.io/en/latest/guide/discovery.html) — recursive scan, extensions, hidden files
- [**Column helpers**](https://csvdir.readthedocs.io/en/latest/guide/columns.html) — single-column or multi-column views with file labels
- [**Pandas integration**](https://csvdir.readthedocs.io/en/latest/guide/pandas.html) — `CsvDirFile` for `pandas.read_csv`
- **Typed** — ships with [`py.typed`](https://github.com/eddiethedean/csvdir/blob/main/csvdir/py.typed) ([API reference](https://csvdir.readthedocs.io/en/latest/reference/index.html))

## Installation

```bash
pip install csvdir
```

Requires **Python 3.10+**. No runtime dependencies. See [Getting started](https://csvdir.readthedocs.io/en/latest/getting-started/) for install and optional extras.

## Quick start

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    print(row)
# {'id': '1', 'name': 'Alice', 'age': '30'}
# {'id': '2', 'name': 'Bob', 'age': '25'}
```

More examples: [Getting started](https://csvdir.readthedocs.io/en/latest/getting-started/)

## Usage

| Topic | Guide |
|-------|--------|
| Row iteration, `with_names()`, `with_paths()` | [Iteration](https://csvdir.readthedocs.io/en/latest/guide/iteration.html) |
| `strict_headers`, `expected_headers`, `on_mismatch` | [Headers](https://csvdir.readthedocs.io/en/latest/guide/headers.html) |
| `chunksize`, `read_dir_chunks` | [Chunking](https://csvdir.readthedocs.io/en/latest/guide/chunking.html) |
| `iter_column`, `select_columns` | [Columns](https://csvdir.readthedocs.io/en/latest/guide/columns.html) |
| `recurse`, `extension`, hidden files | [Discovery](https://csvdir.readthedocs.io/en/latest/guide/discovery.html) |
| `CsvDirFile` + pandas | [Pandas](https://csvdir.readthedocs.io/en/latest/guide/pandas.html) |
| Encodings, BOM, quote sniffing | [Encodings](https://csvdir.readthedocs.io/en/latest/guide/encodings.html) |

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

Details: [Iteration guide](https://csvdir.readthedocs.io/en/latest/guide/iteration.html)

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

Details: [Headers guide](https://csvdir.readthedocs.io/en/latest/guide/headers.html)

### Chunked iteration

```python
for chunk in read_dir("/data/csvs", chunksize=1000):
    process(chunk)  # list[dict[str, str]]
```

Details: [Chunking guide](https://csvdir.readthedocs.io/en/latest/guide/chunking.html)

### Column selection

```python
r = read_dir("/data/csvs")

for name, value in r.with_names().iter_column("name"):
    ...

for name, row in r.with_names().select_columns(["name", "age"]):
    ...
```

Details: [Columns guide](https://csvdir.readthedocs.io/en/latest/guide/columns.html)

### Pandas

```python
import pandas as pd
from csvdir import CsvDirFile

df = pd.read_csv(CsvDirFile("/data/csvs", on_mismatch="skip"))
```

Details: [Pandas guide](https://csvdir.readthedocs.io/en/latest/guide/pandas.html)

## Configuration & API

- [**Full option reference**](https://csvdir.readthedocs.io/en/latest/reference/options.html) — every `read_dir` / `CsvDirFile` parameter
- [**API reference**](https://csvdir.readthedocs.io/en/latest/reference/index.html) — autodoc for all public types and functions
- [**Changelog**](https://csvdir.readthedocs.io/en/latest/CHANGELOG.html)

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

See the [development guide](https://csvdir.readthedocs.io/en/latest/development.html). CI: [`.github/workflows/ci.yml`](https://github.com/eddiethedean/csvdir/blob/main/.github/workflows/ci.yml) (ruff, mypy, pytest on Python 3.10–3.13).

## License

MIT © 2025–2026 — see [LICENSE](https://github.com/eddiethedean/csvdir/blob/main/LICENSE). Release notes: [Changelog](https://csvdir.readthedocs.io/en/latest/CHANGELOG/).
