# File discovery

csvdir finds files before reading them. Discovery is deterministic and configurable.

## Extension matching

```python
read_dir("/data", extension="csv")
```

- Extension is **without** the dot (`"csv"`, not `".csv"`).
- By default `case_insensitive=True` matches `.CSV`, `.Csv`, etc.
- Only **regular files** are included (not directories named `foo.csv`).

## Non-recursive (default)

Only the immediate children of `path` are scanned:

```python
read_dir("/data/inbox")  # does not see /data/inbox/2024/jan.csv unless recurse=True
```

## Recursive scan

```python
read_dir("/data", recurse=True)
```

Uses `os.walk`. Hidden directories (names starting with `.`) are pruned unless `include_hidden=True`.

## Hidden files

Default: skip filenames starting with `.` (e.g. `.backup.csv`).

```python
read_dir("/data", include_hidden=True)
```

Also allows descending into hidden directories when `recurse=True`.

## Missing directory

If `path` does not exist, discovery returns an **empty list** — iteration yields nothing and does not raise.

## Sort order

Matched paths are sorted with Python’s default string sort before iteration. Multi-directory walks produce a flat sorted list of full paths.

## Utilities

Lower-level helpers in `csvdir.pathing`:

| Function | Purpose |
|----------|---------|
| {func}`~csvdir.pathing.get_csv_paths` | List paths with given extension |
| {func}`~csvdir.pathing.get_name` | Stem from a path |
| {func}`~csvdir.pathing._has_extension` | Extension check helper |

## Examples

```python
# All TSV files under tree
read_dir("/imports", extension="tsv", delimiter="\t", recurse=True)

# Only top-level semicolon CSVs
read_dir("/drops", delimiter=";", recurse=False)
```
