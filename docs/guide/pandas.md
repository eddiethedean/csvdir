# Pandas integration

`CsvDirFile` exposes a **single concatenated CSV text stream** (Unicode strings from `read` / `readline`) suitable for [`pandas.read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

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

1. Discover CSV files ([same sorting as dict readers](discovery.md)).
2. Choose a canonical header sequence ([headers guide](headers.md) — sequence-sensitive stitching).
3. Emit that header once, then concatenate **body lines in sorted path order**, matching traversal order used by `read_dir`-style iterators.
4. Subsequent files omit their duplicate header rows when sequences match (`on_mismatch` controls skips vs errors).

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

Header matching for stitching is **order-sensitive** (unlike dict iterators). See [headers](headers.md).

## Restarting reads

```python
f = CsvDirFile("/data")
df1 = pd.read_csv(f)
f.seek(0)
df2 = pd.read_csv(f)
```

## Alternatives

If you need per-file control or **set-based** header matching only (column order may differ across files), iterate paths and load each CSV:

```python
import pandas as pd
from csvdir import read_dir

frames = []
r = read_dir("/data")
for path in r.paths:
    frames.append(pd.read_csv(path))
df = pd.concat(frames, ignore_index=True)
```

For many files with identical schemas (and stitchable sequences), `CsvDirFile` is usually simpler.

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
