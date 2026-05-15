# csvdir

**csvdir** reads every CSV in a directory as one stream of rows. No manual file loops, no surprise headers — just iteration, chunking, and optional pandas integration.

```{toctree}
:maxdepth: 2
:caption: Getting started

installation
quickstart
```

```{toctree}
:maxdepth: 2
:caption: User guide

guide/iteration
guide/headers
guide/chunking
guide/columns
guide/discovery
guide/pandas
guide/encodings
```

```{toctree}
:maxdepth: 2
:caption: Reference

reference/index
reference/options
```

```{toctree}
:maxdepth: 1
:caption: Project

development
changelog
```

## Why csvdir?

Data often arrives as many CSV files in one folder — exports by date, shards by region, or pipeline chunks. **csvdir** gives you:

- A **single iterator** over all files in sorted path order
- **Per-file** encoding and quote detection
- **Header policies** that match real pipelines (strict, skip, or explicit schema)
- **Memory-safe chunking** for large directories
- A **file-like object** for `pandas.read_csv`

The library has **zero runtime dependencies** and ships with type hints (`py.typed`).

## Minimal example

```python
from csvdir import read_dir

for row in read_dir("/data/csvs"):
    print(row["name"])
```

## Public API

| Name | Role |
|------|------|
| {func}`read_dir` | Main factory — row or chunked reader |
| {func}`read_dir_chunks` | Explicit chunked factory |
| {class}`CsvDir` | Row-by-row directory reader |
| {class}`CsvChunksDir` | Fixed-size chunk reader |
| {class}`CsvDirFile` | Concatenated CSV stream for pandas |

See the {doc}`User guide <guide/iteration>` and {doc}`API reference <reference/index>` for full details.
