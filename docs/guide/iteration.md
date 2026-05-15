# Iteration

## `read_dir`

{func}`~csvdir.read_dir` is the main entry point. It discovers CSV files under `path` (default `"."`) and returns either a {class}`~csvdir.CsvDir` or {class}`~csvdir.CsvChunksDir` depending on `chunksize`.

```python
from csvdir import read_dir

reader = read_dir("/exports", extension="csv", delimiter=",")
for row in reader:
    ...
```

### Return type

| `chunksize` | Type | Each iteration yields |
|-------------|------|------------------------|
| `None` (default) | {class}`~csvdir.CsvDir` | `dict[str, str]` |
| positive `int` | {class}`~csvdir.CsvChunksDir` | `list[dict[str, str]]` |

## Row shape

Every row is a plain dictionary:

- **Keys** — header names from the file (BOM stripped from the first column name when present)
- **Values** — strings; missing/`None` cells become `""`

```python
{"id": "42", "name": "Ada", "active": "true"}
```

## File order

Paths come from {func}`~csvdir.pathing.get_csv_paths`, which returns a **sorted** list. Order is stable across runs on the same filesystem.

## Properties

On {class}`~csvdir.CsvDir` (and the chunked reader):

- **`paths`** — `list[str]` of absolute or relative paths to matched files
- **`names`** — `list[str]` of filename stems (extension removed)

```python
r = read_dir("/data")
print(r.paths)   # ['/data/a.csv', '/data/b.csv']
print(r.names)   # ['a', 'b']
```

## Tagged iteration

Helper methods return **new** iterator objects that share the same configuration but attach a file label to each row.

### `with_names()` / `enumerate()`

Alias pair on {class}`~csvdir.CsvDir`. Yields `(stem, row)`:

```python
for stem, row in read_dir("/data").with_names():
    print(stem, row["id"])
```

`stem` is the filename without extension, e.g. `reports_2024` from `reports_2024.csv`.

### `with_paths()`

Yields `(path, row)` with the full path string:

```python
for path, row in read_dir("/data").with_paths():
    print(path, row)
```

On chunked readers, the same helpers yield `(label, chunk)` where `chunk` is `list[dict]`.

## `read_dir_chunks`

Equivalent to `read_dir(path, chunksize=n)` but requires an explicit chunk size:

```python
from csvdir import read_dir_chunks

for chunk in read_dir_chunks("/data", chunksize=500):
    ...
```

Use whichever style reads clearer in your codebase.

## Multiple passes

Iterator objects read from disk lazily. To scan the directory again, create a new `read_dir(...)` call or re-instantiate helpers like `.with_names()`.

{class}`~csvdir.CsvDirFile` supports `seek(0)` to restart the concatenated stream (see {doc}`pandas`).
