# Configuration reference

All parameters below are **keyword-only** after `path` (where `path` is accepted).

## `read_dir` / `CsvDir` / `CsvChunksDir`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str \| None` | `None` | Directory to scan (`"."` when `None`) |
| `extension` | `str` | `"csv"` | File extension without dot |
| `delimiter` | `str` | `","` | Field delimiter |
| `encoding` | `str` | `"utf-8"` | Preferred text encoding |
| `newline` | `str` | `""` | Newline argument to `open()` |
| `quotechar` | `str` | `'"'` | Fallback quote character |
| `escapechar` | `str \| None` | `None` | CSV escape character |
| `chunksize` | `int \| None` | `None` | If set, return `CsvChunksDir` |
| `strict_headers` | `bool` | `False` | Lock schema from first file |
| `expected_headers` | `list[str] \| None` | `None` | Explicit required columns |
| `on_mismatch` | `"error" \| "skip"` | `"error"` | Header mismatch policy |
| `recurse` | `bool` | `False` | Walk subdirectories |
| `case_insensitive` | `bool` | `True` | Case-insensitive extension match |
| `include_hidden` | `bool` | `False` | Include dotfiles and hidden dirs |

## `read_dir_chunks`

Same as above except:

- `chunksize` is **required** (default `1000` in the factory signature)
- Always returns {class}`~csvdir.CsvChunksDir`

## `CsvDirFile`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str \| None` | `None` | Directory to scan |
| `extension` | `str` | `"csv"` | File extension |
| `delimiter` | `str` | `","` | Field delimiter |
| `quotechar` | `str` | `'"'` | Quote character hint |
| `escapechar` | `str \| None` | `None` | Escape character |
| `encoding` | `str` | `"utf-8"` | Preferred encoding |
| `newline` | `str` | `""` | Newline for `open()` |
| `strict_headers` | `bool` | `False` | API symmetry (see headers guide) |
| `expected_headers` | `list[str] \| None` | `None` | Canonical header sequence |
| `on_mismatch` | `str` | `"error"` | `"error"` or `"skip"` |
| `recurse` | `bool` | `False` | Recursive discovery |
| `case_insensitive` | `bool` | `True` | Extension matching |
| `include_hidden` | `bool` | `False` | Hidden files |

## Iterator method matrix

### Row mode (`CsvDir`)

| Method | Yields |
|--------|--------|
| `iter(reader)` | `dict[str, str]` |
| `.with_names()` / `.enumerate()` | `(stem, dict)` |
| `.with_paths()` | `(path, dict)` |
| `.with_names().iter_column(c)` | `(label, str)` |
| `.with_names().select_columns(cols)` | `(label, dict)` |

### Chunk mode (`CsvChunksDir`)

| Method | Yields |
|--------|--------|
| `iter(reader)` | `list[dict]` |
| `.enumerate()` | `(stem, list[dict])` |
| `.with_paths()` | `(path, list[dict])` |
| `.enumerate().iter_column_chunks(c)` | `(label, list[str])` |
| `.enumerate().select_columns_chunks(cols)` | `(label, list[dict])` |
