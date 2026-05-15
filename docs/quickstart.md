# Quickstart

This page walks through the most common patterns in a few minutes.

## Read all rows

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    # row is dict[str, str]
    print(row)
```

Each value is a string (CSV has no native types). `None` from the parser becomes `""`.

## Know which file a row came from

```python
r = read_dir("/data/csvs")

# Filename stem (no extension)
for name, row in r.with_names():
    print(name, row)

# Full path
for path, row in r.with_paths():
    print(path, row)
```

Files are visited in **sorted path order**.

## Skip bad files instead of failing

```python
for row in read_dir(
    "/data/csvs",
    strict_headers=True,
    on_mismatch="skip",
):
    process(row)
```

The first file’s header becomes the schema when `expected_headers` is not set. Later files with different columns are skipped.

## Process in batches

```python
for chunk in read_dir("/data/csvs", chunksize=10_000):
    # chunk is list[dict[str, str]]
    load_to_db(chunk)
```

## Load with pandas

```python
import pandas as pd
from csvdir import CsvDirFile

with CsvDirFile("/data/csvs", on_mismatch="skip") as f:
    df = pd.read_csv(f)
```

## Next steps

- {doc}`guide/headers` — schema validation in depth
- {doc}`guide/chunking` — memory and chunk boundaries
- {doc}`guide/columns` — single-column and multi-column views
- {doc}`reference/options` — every configuration parameter
