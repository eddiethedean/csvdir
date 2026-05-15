# Changelog

## 0.9.0

### Breaking changes

- **`CsvDirFile`:** Stitched body lines stream in **sorted file path order** (aligned with `read_dir`). Canonical header sequence: `expected_headers` if set; else **`strict_headers`** uses the first sorted discovered file; else lexicographically smallest joined header. Match / error / skip behavior follows that path order — callers relying on the previous “emit first matching file out of order” behavior must adapt.

### Additions and fixes

- **`read_dir` / `read_dir_chunks` / `CsvChunksDir`:** Non-positive `chunksize` raises `ValueError`.
- **`get_csv_paths`:** Recursive discovery returns an empty list when `path` does not exist (same as non-recursive).
- **`CsvDir`:** `strict_headers` pins the schema for the iteration without mutating `expected_headers`.

### Packaging, tooling, and docs

- Require Python **3.10+**; PEP 621 / SPDX metadata; typed package.
- CI: ruff, mypy, pytest on 3.10–3.13; `mkdocs build --strict` on docs.
- Remove unused `iterators.py` and `chunks_iterators.py`.
- `read_dir` overloads for clearer return types.
- Documentation on Read the Docs: **MkDocs Material** + **mkdocstrings** (guides, options reference, set vs sequence headers for dict readers vs `CsvDirFile`, pandas example).

## 0.8.0

- Name and path iterator options
- `CsvDirFile` for pandas compatibility
- Keyword-only `extension`, `delimiter`, and `chunksize` parameters

## Earlier releases

See [PyPI release history](https://pypi.org/project/csvdir/#history) for versions 0.7.0 and below.
