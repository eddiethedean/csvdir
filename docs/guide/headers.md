# Headers and schema validation

csvdir can enforce that every file in a directory shares the same columns before yielding rows.

## How matching works (`CsvDir` / `CsvChunksDir`)

Header comparison uses **column names as a set**:

- Order of columns in the file does not matter
- Extra or missing column names trigger a mismatch

```python
# File A: id,name,age
# File B: age,id,name   → OK (same names)

# File C: id,name       → mismatch (missing age)
```

When a mismatch is detected, behavior depends on `on_mismatch`:

| Value | Behavior |
|-------|----------|
| `"error"` (default) | Raise `ValueError` with missing/extra column detail |
| `"skip"` | Skip the entire file (no rows yielded from it) |

## `strict_headers`

```python
read_dir("/data", strict_headers=True)
```

1. Read the **first** file (in sorted path order).
2. Store its header as the expected schema (unless `expected_headers` is already set).
3. For each subsequent file, compare headers to that schema.

Combine with `on_mismatch="skip"` to build a stream from only compatible files:

```python
for row in read_dir("/data", strict_headers=True, on_mismatch="skip"):
    ...
```

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

## `CsvDirFile` (pandas) — different rules

{class}`~csvdir.CsvDirFile` compares headers **in order** (sequence-sensitive) when stitching files. It also picks a **canonical** header row:

- If `expected_headers` is set, that list is canonical.
- Otherwise the lexicographically smallest header (joined by `delimiter`) among discovered files is chosen.

The first file whose header **exactly matches** the canonical sequence supplies the emitted header line; other matching files have their header line skipped. Non-matching files are skipped or raise according to `on_mismatch`.

For dict-based iteration, prefer {class}`~csvdir.CsvDir` semantics. For pandas, understand that column **order** matters in the stitched stream.

## Recipes

### Adopt first file, fail on drift

```python
read_dir("/data", strict_headers=True, on_mismatch="error")
```

### Adopt first file, ignore drift

```python
read_dir("/data", strict_headers=True, on_mismatch="skip")
```

### Fixed contract from code

```python
read_dir("/data", expected_headers=["id", "name", "email"], on_mismatch="skip")
```
