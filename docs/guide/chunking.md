# Chunked reading

Use chunking when you want bounded memory — each iteration returns a list of row dicts instead of a single row.

## Enable chunking

```python
from csvdir import read_dir

for chunk in read_dir("/big_data", chunksize=5000):
    assert isinstance(chunk, list)
    for row in chunk:
        handle(row)
```

Or use the dedicated factory:

```python
from csvdir import read_dir_chunks

for chunk in read_dir_chunks("/big_data", chunksize=5000):
    ...
```

## Chunk boundaries

- Chunks are filled **row by row** within each file, in sorted file order.
- A chunk may span the end of one file and the start of the next if the size limit is hit mid-file.
- The final chunk of a file (and of the full iteration) may be smaller than `chunksize`.
- An empty directory yields nothing (no empty chunks).

## Tagged chunk iteration

```python
r = read_dir("/data", chunksize=100)

for stem, chunk in r.enumerate():
    print(stem, len(chunk))

for path, chunk in r.with_paths():
  ...
```

`enumerate()` is an alias for the stem-based naming used by `with_names()` on the non-chunked reader.

## Column chunks

On enumerated or path-based chunk iterators:

```python
r = read_dir("/data", chunksize=100)

for stem, values in r.enumerate().iter_column_chunks("amount"):
    # values: list[str]
    ...

for stem, rows in r.enumerate().select_columns_chunks(["id", "amount"]):
    # rows: list[dict[str, str]]
    ...
```

See [columns](columns.md) for label semantics (`stem` vs full path).

## When to choose chunk size

| Scenario | Suggestion |
|----------|------------|
| Database bulk insert | Match driver batch size (1k–10k) |
| pandas `DataFrame` construction | Build per chunk with `pd.DataFrame(chunk)` |
| Streaming transform | Small chunks (100–1000) for low latency |

Chunking does not parallelize I/O; it only limits how many rows you hold in a list at once.
