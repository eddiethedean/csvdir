# Pandas integration

{class}`~csvdir.CsvDirFile` exposes a **single concatenated CSV byte stream** suitable for {func}`pandas.read_csv`.

## Basic usage

```python
import pandas as pd
from csvdir import CsvDirFile

f = CsvDirFile("/data/csvs", on_mismatch="skip")
df = pd.read_csv(f)
```

Or with a context manager:

```python
with CsvDirFile("/data/csvs") as f:
    df = pd.read_csv(f)
```

pandas is an **optional** dependency — install separately (`pip install pandas`).

## What `CsvDirFile` does

1. Discover CSV files (same rules as {class}`~csvdir.CsvDir`).
2. Choose a **canonical header** (see {doc}`headers`).
3. Emit the header line once from the first matching file.
4. Stream body lines from each file; skip duplicate header lines when they match exactly.

Data is produced **lazily**; the full directory is not loaded into memory.

## File-like API

| Method | Support |
|--------|---------|
| `read(size=-1)` | Yes |
| `readline()` | Yes |
| `readlines()` | Yes |
| `__iter__` | Yes (lines) |
| `seek(0)` | Restart stream |
| `seek(other)` | `UnsupportedOperation` |
| `tell()` | Logical position |
| `close()` | Release generator |
| Context manager | Yes |

## Configuration

```python
CsvDirFile(
    path="/data",
    extension="csv",
    delimiter=",",
    encoding="utf-8",
    strict_headers=False,
    expected_headers=None,
    on_mismatch="error",
    recurse=False,
    include_hidden=False,
)
```

Header matching for stitching is **order-sensitive** (unlike dict iterators). See {doc}`headers`.

## Restarting reads

```python
f = CsvDirFile("/data")
df1 = pd.read_csv(f)
f.seek(0)
df2 = pd.read_csv(f)
```

## Alternatives

If you need per-file control or set-based header checks, iterate with {class}`~csvdir.CsvDir` and build DataFrames per file:

```python
import pandas as pd
from csvdir import read_dir

frames = [
    pd.DataFrame(list(read_dir.single_file))  # conceptual — use paths + read_csv per path
]
```

For many files with identical schemas, `CsvDirFile` is the ergonomic path.

## Dtype and parse options

Pass any `pandas.read_csv` keyword arguments as usual:

```python
pd.read_csv(
    CsvDirFile("/data"),
    dtype={"id": str},
    parse_dates=["timestamp"],
)
```

csvdir does not interpret types; pandas sees one continuous CSV text stream.
