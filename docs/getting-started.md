# Getting started

csvdir discovers CSV files in a directory and yields each row as a `dict[str, str]` — or in fixed-size chunks when you set `chunksize`. No manual `glob`, no per-file `open` loops.

```{admonition} Requirements
:class: note

- Python 3.10+
- No third-party runtime dependencies (pandas is optional for {class}`~csvdir.CsvDirFile`)
```

## Install

```bash
pip install csvdir
```

From source:

```bash
git clone https://github.com/eddiethedean/csvdir.git
cd csvdir
pip install -e .
```

Optional groups:

```bash
pip install -e ".[dev]"   # pytest, ruff, mypy
pip install -e ".[docs]"  # Sphinx, Furo, MyST
pip install pandas        # only for pandas.read_csv + CsvDirFile
```

## Minimal mental model

1. Point `read_dir` at a directory (default `"."`).
2. Iterate rows — one `dict` per CSV row, all files in sorted path order.
3. Optionally attach file labels with `.with_names()` or `.with_paths()`, or batch rows with `chunksize`.

The [Iteration guide](guide/iteration.md) walks through discovery order, properties, and helper iterators.

## First script

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    print(row)
# {'id': '1', 'name': 'Alice', 'age': '30'}
```

Tagged rows:

```python
for stem, row in read_dir("/data/csvs").with_names():
    print(stem, row["name"])
```

## Where to go next

| Goal | Page |
|------|------|
| Row, path, and name iterators | [Iteration](guide/iteration.md) |
| Schema validation | [Headers](guide/headers.md) |
| Memory-friendly batches | [Chunking](guide/chunking.md) |
| Single or multiple columns | [Columns](guide/columns.md) |
| Recursive scan, extensions | [Discovery](guide/discovery.md) |
| Encodings and quoting | [Encodings](guide/encodings.md) |
| pandas integration | [Pandas](guide/pandas.md) |
| All parameters | [Configuration](reference/options.md) |
| Autodoc | [API reference](reference/index.md) |

## Repository README

Install matrices, usage tables, CI badges, and GitHub doc links live in the canonical [README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md) so PyPI and the repo stay in sync.
