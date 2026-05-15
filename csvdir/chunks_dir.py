from __future__ import annotations

import csv
from collections.abc import Iterator

from .chunks_iter_enum import IterEnumCsvChunksDir
from .chunks_iter_path import IterPathCsvChunksDir
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


class CsvChunksDir:
    """Iterate CSV rows in fixed-size ``list[dict[str, str]]`` chunks.

    ``chunksize`` must be a positive integer.

    Header validation matches {class}`~csvdir.dir_reader.CsvDir`: use
    ``strict_headers``, ``expected_headers``, and ``on_mismatch`` (``'error'`` or ``'skip'``).
    """

    def __init__(
        self,
        chunksize: int,
        path: str | None,
        extension: str = "csv",
        delimiter: str = ",",
        encoding: str = "utf-8",
        newline: str = "",
        quotechar: str = '"',
        escapechar: str | None = None,
        strict_headers: bool = False,
        expected_headers: list[str] | None = None,
        on_mismatch: str = "error",
        recurse: bool = False,
        case_insensitive: bool = True,
        include_hidden: bool = False,
    ) -> None:
        cs = int(chunksize)
        if cs <= 0:
            raise ValueError("chunksize must be a positive integer")
        self.chunksize = cs
        self.path = path
        self.extension = extension
        self.delimiter = delimiter
        self.encoding = encoding
        self.newline = newline
        self.quotechar = quotechar
        self.escapechar = escapechar
        self.strict_headers = strict_headers
        self.expected_headers = list(expected_headers) if expected_headers else None
        self.on_mismatch = on_mismatch
        self.recurse = recurse
        self.case_insensitive = case_insensitive
        self.include_hidden = include_hidden

    # ---------------- core iteration ----------------

    def __iter__(self) -> Iterator[list[dict[str, str]]]:
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

            # open file with encoding + quote sniffing
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
                        yield chunk
                        chunk = []
                if chunk:
                    yield chunk

    # ---------------- helper iterators ----------------

    def with_paths(self) -> IterPathCsvChunksDir:
        """
        Return an iterator yielding (path, chunk) pairs.
        """
        return IterPathCsvChunksDir(
            self.chunksize,
            self.path,
            extension=self.extension,
            delimiter=self.delimiter,
            encoding=self.encoding,
            newline=self.newline,
            quotechar=self.quotechar,
            escapechar=self.escapechar,
            strict_headers=self.strict_headers,
            expected_headers=list(self.expected_headers) if self.expected_headers else None,
            on_mismatch=self.on_mismatch,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        )

    def enumerate(self) -> IterEnumCsvChunksDir:
        """
        Return an iterator yielding (name, chunk) pairs, where `name` is the stem from the path.
        """
        return IterEnumCsvChunksDir(
            self.chunksize,
            self.path,
            extension=self.extension,
            delimiter=self.delimiter,
            encoding=self.encoding,
            newline=self.newline,
            quotechar=self.quotechar,
            escapechar=self.escapechar,
            strict_headers=self.strict_headers,
            expected_headers=list(self.expected_headers) if self.expected_headers else None,
            on_mismatch=self.on_mismatch,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        )
