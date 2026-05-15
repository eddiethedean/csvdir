# Headers and schema validation

csvdir can enforce that every file in a directory shares the same columns before yielding rows.

## How matching works (`CsvDir` / `CsvChunksDir`)

Header comparison uses **column names as a set**:

- Order of columns in the file does not matter across files covered by dict readers
- Extra or missing column names trigger a mismatch

```python
# File A: id,name,age
# File B: age,id,name   → OK (same names)

# File C: id,name       → mismatch (missing age)
```

When that kind of mismatch is detected, behavior depends on `on_mismatch`:

| Value | Behavior |
|-------|----------|
| `"error"` (default) | Raise `ValueError` with missing/extra column detail |
| `"skip"` | Skip the entire file (no rows yielded from it) |

### Regression check: reorder vs `CsvDirFile`

Because matching is **set-based**, permuting header order between files **does not** count as mismatch for `read_dir`:

```python
# aaa.csv  →  id,name
# zzz.csv  →  name,id   → still OK for read_dir(...)
```

[`CsvDirFile`](pandas.md) requires the header **sequence** to match — see below.

## `strict_headers`

```python
read_dir("/data", strict_headers=True)
```

1. Read files in sorted path order (see [Discovery](discovery.md)).
2. The **first file’s column set** establishes the pinned schema unless `expected_headers` is already set.
3. For each subsequent file, compare headers to that schema (**order ignored**).

Combine with `on_mismatch="skip"` to build a stream from only compatible files:

```python
for row in read_dir("/data", strict_headers=True, on_mismatch="skip"):
    ...
```

Iteration does **not** mutate the `CsvDir.expected_headers` field; the pinned schema applies only inside that iteration.

## `expected_headers`

Supply an explicit schema that every file must match:

```python
SCHEMA = ["id", "timestamp", "value"]

for row in read_dir("/data", expected_headers=SCHEMA):
    ...
```

You do not need `strict_headers=True` when `expected_headers` is provided — the list is always enforced.

## Error messages

Mismatch errors look like:

```text
ValueError: Header mismatch in '/data/bad.csv': missing columns: ['age']; extra columns: ['years']
```

## `CsvDirFile` (pandas) — stricter stitching rules

`CsvDirFile` builds one physical CSV header line followed by concatenated bodies. Stitching compares headers **in order** (sequence-sensitive): the emitted header establishes column order, and subsequent files must match that header line exactly (after normalization). That is stronger than dict iterators, which compare **sets** of names.

Choose the canonical sequence this way:

- If `expected_headers` is set, that list defines canonical column order.
- Else if `strict_headers` is True, canonical order is taken from **the first discovered file** in sorted path order (same sorting as `CsvDir`). Name files so your intended baseline sorts first — e.g. `aaa_main.csv`, `zzz_extra.csv`.

Otherwise the canonical sequence is the lexicographically smallest `delimiter`-joined header among scanned files.

**Row order:** body lines appear in sorted file path order, matching traversal order used by [`CsvDir`](iteration.md).

For pandas, assume column **order** in the stitched stream matters. For tolerant column-set matching alone, iterate with [`read_dir`](../getting-started.md) first.

## Recipes (`read_dir`)

### Pin first file schema, fail on drift

```python
read_dir("/data", strict_headers=True, on_mismatch="error")
```

### Pin first file schema, skip incompatible files

```python
read_dir("/data", strict_headers=True, on_mismatch="skip")
```

### Fixed contract from code

```python
read_dir("/data", expected_headers=["id", "name", "email"], on_mismatch="skip")
```
