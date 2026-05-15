# Encodings, BOM, and quoting

csvdir handles messy real-world CSV files per file — encoding and quote character can differ between files in the same directory.

## Preferred encoding

```python
read_dir("/data", encoding="utf-8")
```

Each file is opened using `utils.pick_encoding`, which:

1. Tries the preferred encoding
2. Falls back through `utf-8`, `utf-8-sig`, `utf-16-le`, `utf-16-be`
3. Rejects decodes that contain NUL bytes (common mis-decode signal)

## BOM in headers

UTF-8 BOM markers are stripped from **header names** after read:

```python
# File header cell: "\ufeffid,name"
# Yielded dict keys: "id", "name"
```

`CsvDirFile` also strips BOM from the emitted header **line** in the stitched stream.

## Quote character sniffing

`utils.sniff_quotechar` inspects a sample of each file:

1. Prefer a quote char that wraps fields containing the delimiter
2. Try `csv.Sniffer`
3. Fall back to configured `quotechar` (default `"`)

You can still set `quotechar` explicitly; it acts as a fallback when sniffing is inconclusive.

## Delimiter and escape

```python
read_dir("/data", delimiter=";", escapechar="\\")
```

Passed through to the stdlib `csv` module for that file.

## Newline

```python
read_dir("/data", newline="")
```

The recommended value for `csv` module compatibility (platform newlines inside quoted fields still work).

## Mixed encodings in one directory

This is supported: each file is opened with its own detected encoding. There is no global assumption that all files share one encoding. The same mechanism applies when [`CsvDirFile`](pandas.md) opens each file while building the stitched stream.

## Limitations

- Detection reads a **prefix** of each file (first 2–4 KB). Files that change encoding mid-stream are not supported.
- csvdir does not transcode to a common encoding; consumers see Unicode `str` rows after decode.
- Binary CSV-like files that decode without error but parse incorrectly may still require manual filtering.

## Related utilities

| Function | Role |
|----------|------|
| `utils.pick_encoding` | Choose encoding for a path |
| `utils.sniff_quotechar` | Detect quote character |
| `utils.read_header` | Read header row with detection |
| `utils.strip_bom_from_headers` | Clean header list |
