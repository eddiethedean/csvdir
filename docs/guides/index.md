# Guides

Step-by-step documentation for every major feature. Start with [Getting started](../getting-started.md) if you are new to csvdir.

## Core workflows

| Guide | Topics |
|-------|--------|
| [Iteration](../guide/iteration.md) | `read_dir`, `CsvDir`, `with_names`, `with_paths`, file order |
| [Headers](../guide/headers.md) | Set vs sequence headers (`read_dir` vs `CsvDirFile`), `strict_headers`, `expected_headers`, `on_mismatch` |
| [Chunking](../guide/chunking.md) | `chunksize ≥ 1`, `read_dir_chunks`, column chunks |
| [Columns](../guide/columns.md) | `iter_column`, `select_columns`, labels |

## Files and formats

| Guide | Topics |
|-------|--------|
| [Discovery](../guide/discovery.md) | `recurse`, `extension`, hidden files |
| [Encodings](../guide/encodings.md) | BOM, sniffing, mixed encodings per file |
| [Pandas](../guide/pandas.md) | `CsvDirFile`, `read_csv`, streaming |

## Reference

| Page | Topics |
|------|--------|
| [Configuration](../reference/options.md) | Full parameter tables |
| [API reference](../reference/api.md) | Autodoc for all public symbols |
