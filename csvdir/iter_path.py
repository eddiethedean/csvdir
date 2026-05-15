from __future__ import annotations

import csv
from collections.abc import Generator, Iterator
from dataclasses import dataclass, field

from .pathing import get_csv_paths
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
class IterPathCsvDir:
    path: str | None = None
    extension: str = "csv"
    delimiter: str = ","
    encoding: str = "utf-8"
    newline: str = ""
    quotechar: str = '"'
    escapechar: str | None = None
    strict_headers: bool = False
    expected_headers: list[str] | None = None
    on_mismatch: str = "error"  # 'error' or 'skip'
    # directory walking options
    recurse: bool = False
    case_insensitive: bool = True
    include_hidden: bool = False

    # internal generator state for iterator protocol
    _it: Generator[tuple[str, dict[str, str]], None, None] | None = field(
        init=False, default=None, repr=False
    )

    # ---------- iterator protocol ----------

    def __iter__(self) -> IterPathCsvDir:
        self._it = self._gen()
        return self

    def __next__(self) -> tuple[str, dict[str, str]]:
        if self._it is None:
            self._it = self._gen()
        return next(self._it)

    def _gen(self) -> Generator[tuple[str, dict[str, str]], None, None]:
        canonical = list(self.expected_headers) if self.expected_headers else None
        for p in get_csv_paths(
            self.path or ".",
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        ):
            # header check
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

            # open with chosen encoding + quote sniff
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

                for row in reader:
                    yield (p, {k: ("" if v is None else str(v)) for k, v in row.items()})

    # ---------- column selection helpers ----------

    def iter_column(self, column_name: str) -> Iterator[tuple[str, str]]:
        """
        Yield (path, value) for a single column across files.

        If the requested column is missing in a file:
          - on_mismatch == "skip": skip that file
          - on_mismatch == "error": raise ValueError
        """
        canonical = list(self.expected_headers) if self.expected_headers else None
        for p in get_csv_paths(
            self.path or ".",
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        ):
            # header check
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

                for row in reader:
                    v = row.get(column_name)
                    yield (p, "" if v is None else str(v))

    def select_columns(self, columns: list[str]) -> Iterator[tuple[str, dict[str, str]]]:
        """
        Yield (path, {subset}) per row for the requested columns.

        If any requested column is missing in a file:
          - on_mismatch == "skip": skip that file
          - on_mismatch == "error": raise ValueError
        """
        canonical = list(self.expected_headers) if self.expected_headers else None
        for p in get_csv_paths(
            self.path or ".",
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        ):
            # header check
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

                for row in reader:
                    out: dict[str, str] = {}
                    for c in columns:
                        v = row.get(c)
                        out[c] = "" if v is None else str(v)
                    yield (p, out)
