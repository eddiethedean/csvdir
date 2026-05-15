from __future__ import annotations

import io
from collections.abc import Iterator
from dataclasses import dataclass

from .pathing import get_csv_paths
from .utils import pick_encoding
from .utils import read_header as _read_header


def _strip_bom_from_line(s: str) -> str:
    if s and s[0] == "\ufeff":
        return s[1:]
    return s


def _headers_match_seq(file_headers: list[str], canonical: list[str]) -> bool:
    return list(file_headers) == list(canonical)


@dataclass
class CsvDirFile:
    """
    File-like object that concatenates CSV files in a directory into one logical CSV stream.
    Emit one header line, then bodies in **sorted file path order**
    (same discovery order as ``CsvDir``).

    Stitching compares headers **in sequence** — the emitted header fixes column order.
    ``CsvDir`` / ``read_dir`` treat header **names as sets**, so columns may be permuted
    across files.

    Canonical header sequence:

    - If ``expected_headers`` is set, that list is canonical.
    - Else if ``strict_headers`` is true, use the **first discovered** file after sorting
      (same rule as ``CsvDir``).
    - Else choose the lexicographically smallest ``delimiter``.join(headers) among scanned files.

    Matching files contribute their body lines after the sole header emit; mismatches skip or raise
    according to ``on_mismatch``.

    pandas compatibility:

    - read(size=-1), readline(), readlines(); ``size`` uses Python string/code-unit counts.
    - seek(0) to restart (other seeks raise).
    - tell(), readable(), seekable(), close(), context manager.

    Data is lazy; directory contents are not fully buffered in memory.
    """

    # Directory scanning
    path: str | None = None
    extension: str = "csv"
    recurse: bool = False
    case_insensitive: bool = True
    include_hidden: bool = False

    # Header parsing / canonical selection
    delimiter: str = ","
    quotechar: str = '"'
    escapechar: str | None = None

    # IO options
    encoding: str = "utf-8"
    newline: str = ""

    # Header policy
    strict_headers: bool = False
    expected_headers: list[str] | None = None
    on_mismatch: str = "error"  # "error" or "skip"

    # Internal streaming state
    _gen: Iterator[str] | None = None  # line generator for the stitched stream
    _buf: str = ""  # unread tail from last read
    _pos: int = 0  # logical position in the concatenated stream
    _closed: bool = False

    # -------------------- std io API --------------------

    def __enter__(self) -> CsvDirFile:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        self._gen = None
        self._buf = ""
        self._closed = True

    @property
    def closed(self) -> bool:
        return self._closed

    def readable(self) -> bool:
        return not self._closed

    def seekable(self) -> bool:
        # We support seek(0) (restart). Other seeks raise UnsupportedOperation.
        return True

    def tell(self) -> int:
        return self._pos

    def seek(self, offset: int, whence: int = 0) -> int:
        if self._closed:
            raise ValueError("I/O operation on closed CsvDirFile")
        if whence == 0 and offset == 0:
            # restart stream
            self._reset_stream()
            return self._pos
        if whence == 1 and offset == 0:
            # no-op
            return self._pos
        raise io.UnsupportedOperation("CsvDirFile only supports seek(0, 0) and seek(0, 1)")

    # Iteration yields lines
    def __iter__(self) -> Iterator[str]:
        while True:
            line = self.readline()
            if not line:
                break
            yield line

    # Size-bounded read
    def read(self, size: int = -1) -> str:
        self._ensure_gen()
        if size is None or size < 0:
            # drain everything
            chunks = [self._buf]
            self._pos += len(self._buf)
            self._buf = ""
            gen = self._gen
            assert gen is not None
            for line in gen:
                chunks.append(line)
                self._pos += len(line)
            return "".join(chunks)

        # ensure at least size bytes in buffer (or EOF)
        out = io.StringIO()
        while len(self._buf) < size:
            nxt = self._next_line_or_eof()
            if nxt is None:
                break
            self._buf += nxt
        # slice out requested bytes
        take = self._buf[:size]
        self._buf = self._buf[size:]
        self._pos += len(take)
        out.write(take)
        return out.getvalue()

    def readline(self) -> str:
        self._ensure_gen()
        # fill buffer until newline or EOF
        idx = self._buf.find("\n")
        while idx < 0:
            nxt = self._next_line_or_eof()
            if nxt is None:
                break
            self._buf += nxt
            idx = self._buf.find("\n")

        if idx >= 0:
            # include newline
            line = self._buf[: idx + 1]
            self._buf = self._buf[idx + 1 :]
        else:
            # last line without newline (EOF)
            line = self._buf
            self._buf = ""

        self._pos += len(line)
        return line

    def readlines(self) -> list[str]:
        lines: list[str] = []
        while True:
            ln = self.readline()
            if not ln:
                break
            lines.append(ln)
        return lines

    # -------------------- internals --------------------

    def _reset_stream(self) -> None:
        self._gen = None
        self._buf = ""
        self._pos = 0
        self._closed = False
        self._ensure_gen()

    def _ensure_gen(self) -> None:
        if self._closed:
            raise ValueError("I/O operation on closed CsvDirFile")
        if self._gen is None:
            self._gen = self._line_generator()

    def _next_line_or_eof(self) -> str | None:
        assert self._gen is not None
        try:
            return next(self._gen)
        except StopIteration:
            return None

    def _line_generator(self) -> Iterator[str]:
        """Yield one stitched CSV stream: single header row, bodies in sorted path order."""
        base = self.path or "."
        paths = get_csv_paths(
            base,
            self.extension,
            recurse=self.recurse,
            case_insensitive=self.case_insensitive,
            include_hidden=self.include_hidden,
        )
        if not paths:
            return

        header_index = [
            (
                p,
                _read_header(
                    p,
                    encoding=self.encoding,
                    newline=self.newline,
                    delimiter=self.delimiter,
                    quotechar=self.quotechar,
                    escapechar=self.escapechar,
                ),
            )
            for p in paths
        ]
        hdr_map = dict(header_index)

        # Canonical sequence (aligned with stitching rules in class docstring)
        if self.expected_headers:
            canonical = list(self.expected_headers)
        elif self.strict_headers:
            canonical = list(header_index[0][1])
        else:

            def _key(hs: list[str]) -> str:
                return self.delimiter.join(hs)

            canonical = min((hs for _, hs in header_index), key=_key)

        emitted_header = False
        for p in paths:
            hs = hdr_map[p]
            if not _headers_match_seq(hs, canonical):
                if self.on_mismatch == "skip":
                    continue
                raise ValueError(f"Header mismatch in '{p}': expected {canonical} got {hs}")

            enc = pick_encoding(p, self.encoding, self.newline)
            with open(p, encoding=enc, newline=self.newline) as f:
                header_line = f.readline()
                header_line = _strip_bom_from_line(header_line)
                if header_line and not header_line.endswith(("\n", "\r")):
                    header_line += "\n"

                if not emitted_header:
                    if header_line:
                        yield header_line
                    emitted_header = True
                # else: header line discarded; body streamed next
                yield from f


__all__ = ["CsvDirFile"]
