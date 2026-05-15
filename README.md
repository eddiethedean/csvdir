# csvdir

[![CI](https://github.com/eddiethedean/csvdir/actions/workflows/ci.yml/badge.svg)](https://github.com/eddiethedean/csvdir/actions/workflows/ci.yml) [![Docs](https://readthedocs.org/projects/csvdir/badge/?version=latest)](https://csvdir.readthedocs.io/en/latest/) [![PyPI](https://img.shields.io/pypi/v/csvdir.svg)](https://pypi.org/project/csvdir/) [![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Feddiethedean%2Fcsvdir%2Fmain%2Fpyproject.toml)](https://github.com/eddiethedean/csvdir/blob/main/pyproject.toml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/eddiethedean/csvdir/blob/main/LICENSE)

**Read every CSV in a directory as one stream of rows.** No manual file loops, no header surprises — discovery, encoding, chunking, and optional pandas integration.

**Documentation (primary):** **[csvdir.readthedocs.io](https://csvdir.readthedocs.io/en/latest/)** — getting started, guides, configuration, API reference, and changelog.

## At a glance

| Without csvdir | With csvdir |
|----------------|-------------|
| Loop `glob` + `open` per file | `read_dir("/data")` yields every row |
| Header drift breaks pipelines | `strict_headers` / `on_mismatch="skip"` |
| Load huge dirs into memory | `chunksize=` streams `list[dict]` batches |
| Awkward pandas glue code | `CsvDirFile` works with `pandas.read_csv` |

**Includes:** row and chunked iterators, `.with_names()` / `.with_paths()`, column helpers, recursive discovery, per-file encoding and quote sniffing. Dict iterators compare header **names as sets**; `CsvDirFile` (pandas) stitches using header **sequence** and sorted path order — see docs.

## Requirements

Python **3.10+**. No runtime dependencies (pandas optional for `CsvDirFile`).

## Install

```bash
pip install csvdir
```

From a clone (contributors):

```bash
git clone https://github.com/eddiethedean/csvdir.git
cd csvdir
pip install -e ".[dev]"
```

## Quick start

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    print(row)
```

```python
for stem, row in read_dir("/data/csvs").with_names():
    print(stem, row["name"])
```

More patterns (headers, chunks, columns, pandas) are in the **guides** on Read the Docs.

## Documentation map

| Start here | Read the Docs |
|------------|---------------|
| Install & mental model | [Getting started](https://csvdir.readthedocs.io/en/latest/getting-started/) |
| Feature guides | [Guides overview](https://csvdir.readthedocs.io/en/latest/guides/) |
| Every `read_dir` option | [Configuration](https://csvdir.readthedocs.io/en/latest/reference/options/) |
| Autodoc | [API reference](https://csvdir.readthedocs.io/en/latest/reference/api/) |
| Release history | [Changelog](https://csvdir.readthedocs.io/en/latest/CHANGELOG/) |

Design files remain in `docs/` in the repo; the site above is the supported reading path for releases.

## Contributing

```bash
pip install -e ".[dev,docs]"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
ruff check csvdir tests && ruff format --check csvdir tests
mypy
python -m mkdocs build --strict
```

CI runs the same checks on Python 3.10–3.13. See [Development](https://csvdir.readthedocs.io/en/latest/development/) on RTD.

## License

MIT — [LICENSE](https://github.com/eddiethedean/csvdir/blob/main/LICENSE).
