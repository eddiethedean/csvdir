# Column selection

Column helpers let you project one or more fields while keeping a **file label** on each yielded value. They are available on **tagged** iterators, not on the bare `for row in read_dir(...)` loop.

## Which object to use?

| Goal | Iterator | Column methods |
|------|----------|----------------|
| Label = filename stem | `.with_names()` or `.enumerate()` | `.iter_column`, `.select_columns` |
| Label = full path | `.with_paths()` | same |
| Chunked | `.enumerate()` / `.with_paths()` on chunked reader | `.iter_column_chunks`, `.select_columns_chunks` |

## Single column

```python
r = read_dir("/data")

for stem, value in r.with_names().iter_column("email"):
    print(stem, value)
```

```python
for path, value in r.with_paths().iter_column("email"):
    print(path, value)
```

If the column is missing and `on_mismatch="error"`, a `ValueError` is raised. With `"skip"`, the file is skipped.

## Multiple columns

```python
for stem, row in r.with_names().select_columns(["id", "name"]):
    # row only contains requested keys
    print(stem, row)
```

Keys not present in the file still follow dict access rules (KeyError if absent from the row dict after read).

## Chunked column values

```python
for stem, values in read_dir("/data", chunksize=50).enumerate().iter_column_chunks("score"):
    print(stem, values)  # list[str], len <= 50
```

```python
for stem, rows in read_dir("/data", chunksize=50).enumerate().select_columns_chunks(
    ["id", "score"]
):
    print(stem, rows)  # list[dict]
```

Optional `chunk_size` argument on chunk methods overrides the reader’s default `chunksize` for that call.

## Label format note

- **`with_names()` / `enumerate()`** — stem without extension (`sales_q1`)
- **`with_paths()`** — full path string (`/data/2024/sales_q1.csv`)

Tests for enumerate-style iterators may use the filename with extension in some code paths; prefer `with_names()` for stems consistently.

## Compare to manual projection

```python
# Manual
for row in read_dir("/data"):
    print(row["email"])

# With file attribution
for stem, email in read_dir("/data").with_names().iter_column("email"):
    print(stem, email)
```

Use column helpers when you need **per-file** provenance on each value or chunk.
