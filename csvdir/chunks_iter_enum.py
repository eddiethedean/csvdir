from __future__ import annotations

import csv
import os
from collections.abc import Generator, Iterator
from dataclasses import dataclass, field

from .pathing import get_csv_paths, get_name
from .utils import (
    check_headers as _check_headers,
)
from .utils import (
    pick_encoding,
    sniff_quotechar,
    strip_bom_from_headers,
)
from .utils import (
    read_header as _read_header,
)


@dataclass(slots=True)
class IterEnumCsvChunksDir:
    """
    Chunked enumerating iterator over a directory of CSVs.

    Test expectations:
      - enumerate() yields (stem_without_ext, chunk_of_row_dicts)
      - iter_column_chunks()/select_columns_chunks() yield (filename_with_ext, chunk)
    """

    chunksize: int
    path: str | None = None
    extension: str = "csv"
    delimiter: str = ","
    encoding: str = "utf-8"
    newline: str = ""
    quotechar: str = '"'
    escapechar: str | None = None
    strict_headers: bool = False
    expected_headers: list[str] | None = None
    on_mismatch: str = "error"
    recurse: bool = False
    case_insensitive: bool = True
    include_hidden: bool = False

    _it: Generator[tuple[str, list[dict[str, str]]], None, None] | None = field(
        init=False, default=None, repr=False
    )

    # ---------------- core iterator protocol ----------------

    def __iter__(self) -> IterEnumCsvChunksDir:
        self._it = self._gen()
        return self

    def __next__(self) -> tuple[str, list[dict[str, str]]]:
        if self._it is None:
            self._it = self._gen()
        return next(self._it)

    def _gen(self) -> Generator[tuple[str, list[dict[str, str]]], None, None]:
        canonical = list(self.expected_headers) if self.expected_headers else None

        for p in get_csv_paths(
            self.path or ".",
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        ):
            file_headers = _read_header(
                p,
                encoding=self.encoding,
                newline=self.newline,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                escapechar=self.escapechar,
            )

            if self.strict_headers and canonical is None:
                canonical = file_headers

            expected = canonical or self.expected_headers
            if expected is not None:
                match, missing, extra = _check_headers(file_headers, expected)
                if not match:
                    if self.on_mismatch == "skip":
                        continue
                    detail: list[str] = []
                    if missing:
                        detail.append(f"missing columns: {missing}")
                    if extra:
                        detail.append(f"extra columns: {extra}")
                    raise ValueError(f"Header mismatch in '{p}': " + "; ".join(detail))

            # enumerate() (chunked) → STEM (no extension)
            name = get_name(p)

            enc = pick_encoding(p, self.encoding, self.newline)
            with open(p, newline=self.newline, encoding=enc) as f:
                qc = sniff_quotechar(
                    p,
                    delimiter=self.delimiter,
                    encoding=enc,
                    newline=self.newline,
                    fallback=self.quotechar or '"',
                )
                reader = csv.DictReader(
                    f,
                    delimiter=self.delimiter,
                    quotechar=qc,
                    escapechar=self.escapechar,
                )
                if reader.fieldnames:
                    reader.fieldnames = strip_bom_from_headers(reader.fieldnames)

                chunk: list[dict[str, str]] = []
                for row in reader:
                    chunk.append({k: ("" if v is None else str(v)) for k, v in row.items()})
                    if len(chunk) >= self.chunksize:
                        yield (name, chunk)
                        chunk = []
                if chunk:
                    yield (name, chunk)

    # -------- column selection helpers (chunked) → names WITH extension --------

    def iter_column_chunks(
        self, column_name: str, chunk_size: int | None = None
    ) -> Iterator[tuple[str, list[str]]]:
        cs = self.chunksize if chunk_size is None else int(chunk_size)
        canonical = list(self.expected_headers) if self.expected_headers else None

        for p in get_csv_paths(
            self.path or ".",
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        ):
            file_headers = _read_header(
                p,
                encoding=self.encoding,
                newline=self.newline,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                escapechar=self.escapechar,
            )

            if self.strict_headers and canonical is None:
                canonical = file_headers

            expected = canonical or self.expected_headers
            if expected is not None:
                match, missing, extra = _check_headers(file_headers, expected)
                if not match:
                    if self.on_mismatch == "skip":
                        continue
                    detail: list[str] = []
                    if missing:
                        detail.append(f"missing columns: {missing}")
                    if extra:
                        detail.append(f"extra columns: {extra}")
                    raise ValueError(f"Header mismatch in '{p}': " + "; ".join(detail))

            if column_name not in file_headers:
                if self.on_mismatch == "skip":
                    continue
                raise ValueError(f"Column '{column_name}' not found in '{p}'")

            # column helpers (chunked) → filename WITH extension
            name = os.path.basename(p)

            enc = pick_encoding(p, self.encoding, self.newline)
            with open(p, encoding=enc, newline=self.newline) as f:
                qc = sniff_quotechar(
                    p,
                    delimiter=self.delimiter,
                    encoding=enc,
                    newline=self.newline,
                    fallback=self.quotechar or '"',
                )
                reader = csv.DictReader(
                    f,
                    delimiter=self.delimiter,
                    quotechar=qc,
                    escapechar=self.escapechar,
                )
                if reader.fieldnames:
                    reader.fieldnames = strip_bom_from_headers(reader.fieldnames)

                out: list[str] = []
                for row in reader:
                    v = row.get(column_name)
                    out.append("" if v is None else str(v))
                    if len(out) >= cs:
                        yield (name, out)
                        out = []
                if out:
                    yield (name, out)

    def select_columns_chunks(
        self, columns: list[str], chunk_size: int | None = None
    ) -> Iterator[tuple[str, list[dict[str, str]]]]:
        cs = self.chunksize if chunk_size is None else int(chunk_size)
        canonical = list(self.expected_headers) if self.expected_headers else None

        for p in get_csv_paths(
            self.path or ".",
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        ):
            file_headers = _read_header(
                p,
                encoding=self.encoding,
                newline=self.newline,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                escapechar=self.escapechar,
            )

            if self.strict_headers and canonical is None:
                canonical = file_headers

            expected = canonical or self.expected_headers
            if expected is not None:
                match, missing, extra = _check_headers(file_headers, expected)
                if not match:
                    if self.on_mismatch == "skip":
                        continue
                    detail: list[str] = []
                    if missing:
                        detail.append(f"missing columns: {missing}")
                    if extra:
                        detail.append(f"extra columns: {extra}")
                    raise ValueError(f"Header mismatch in '{p}': " + "; ".join(detail))

            missing_req = [c for c in columns if c not in file_headers]
            if missing_req:
                if self.on_mismatch == "skip":
                    continue
                raise ValueError(f"Missing requested columns in '{p}': {missing_req}")

            # column helpers (chunked) → filename WITH extension
            name = os.path.basename(p)

            enc = pick_encoding(p, self.encoding, self.newline)
            with open(p, encoding=enc, newline=self.newline) as f:
                qc = sniff_quotechar(
                    p,
                    delimiter=self.delimiter,
                    encoding=enc,
                    newline=self.newline,
                    fallback=self.quotechar or '"',
                )
                reader = csv.DictReader(
                    f,
                    delimiter=self.delimiter,
                    quotechar=qc,
                    escapechar=self.escapechar,
                )
                if reader.fieldnames:
                    reader.fieldnames = strip_bom_from_headers(reader.fieldnames)

                out: list[dict[str, str]] = []
                for row in reader:
                    item: dict[str, str] = {}
                    for c in columns:
                        v = row.get(c)
                        item[c] = "" if v is None else str(v)
                    out.append(item)
                    if len(out) >= cs:
                        yield (name, out)
                        out = []
                if out:
                    yield (name, out)
