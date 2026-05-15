# Changelog

## 0.9.1 (unreleased)

- **Breaking (stitch semantics):** `CsvDirFile` now streams bodies in sorted path order (aligned with dict iterators); canonical header picking honors `strict_headers` (first discovered file defines column order unless `expected_headers` is set). Error/skip sequencing follows path order strictly.
- `read_dir` / `read_dir_chunks` reject non-positive `chunksize` with `ValueError`.
- Recursive `get_csv_paths` mirrors flat mode and returns `[]` when `path` does not exist.
- `CsvDir` iteration no longer mutates `expected_headers` when pinning `strict_headers` schema internally.
- Guides and configuration reference refreshed: `chunksize` validation, missing-directory recursion, set vs sequence headers (`read_dir` vs `CsvDirFile`), stitched row order, and pandas workaround example.

## 0.9.0

- Require Python 3.10+
- Modern packaging (PEP 621, SPDX license, typed package)
- CI with ruff, mypy, and pytest on 3.10–3.13
- Remove unused `iterators.py` and `chunks_iterators.py` modules
- `read_dir` overloads for clearer return types
- Documentation on Read the Docs (MkDocs/material + mkdocstrings)

## 0.8.0

- Name and path iterator options
- `CsvDirFile` for pandas compatibility
- Keyword-only `extension`, `delimiter`, and `chunksize` parameters

## Earlier releases

See [PyPI release history](https://pypi.org/project/csvdir/#history) for versions 0.7.0 and below.
