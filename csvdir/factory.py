from __future__ import annotations

from typing import Literal, overload

from .chunks_dir import CsvChunksDir
from .dir_reader import CsvDir


@overload
def read_dir(
    path: str | None = None,
    *,
    extension: str = "csv",
    delimiter: str = ",",
    chunksize: None = None,
    encoding: str = "utf-8",
    newline: str = "",
    quotechar: str = '"',
    escapechar: str | None = None,
    strict_headers: bool = False,
    expected_headers: list[str] | None = None,
    on_mismatch: Literal["error", "skip"] = "error",
    recurse: bool = False,
    case_insensitive: bool = True,
    include_hidden: bool = False,
) -> CsvDir: ...


@overload
def read_dir(
    path: str | None = None,
    *,
    extension: str = "csv",
    delimiter: str = ",",
    chunksize: int,
    encoding: str = "utf-8",
    newline: str = "",
    quotechar: str = '"',
    escapechar: str | None = None,
    strict_headers: bool = False,
    expected_headers: list[str] | None = None,
    on_mismatch: Literal["error", "skip"] = "error",
    recurse: bool = False,
    case_insensitive: bool = True,
    include_hidden: bool = False,
) -> CsvChunksDir: ...


def read_dir(
    path: str | None = None,
    *,
    extension: str = "csv",
    delimiter: str = ",",
    chunksize: int | None = None,
    encoding: str = "utf-8",
    newline: str = "",
    quotechar: str = '"',
    escapechar: str | None = None,
    strict_headers: bool = False,
    expected_headers: list[str] | None = None,
    on_mismatch: Literal["error", "skip"] = "error",
    recurse: bool = False,
    case_insensitive: bool = True,
    include_hidden: bool = False,
) -> CsvDir | CsvChunksDir:
    """Discover and iterate CSV files under ``path``.

    Returns {class}`~csvdir.chunks_dir.CsvChunksDir` when ``chunksize`` is set,
    otherwise {class}`~csvdir.dir_reader.CsvDir`.
    """
    if chunksize:
        return CsvChunksDir(
            chunksize,
            path,
            extension,
            delimiter,
            encoding,
            newline,
            quotechar,
            escapechar,
            strict_headers,
            expected_headers,
            on_mismatch,
            recurse,
            case_insensitive,
            include_hidden,
        )
    return CsvDir(
        path,
        extension,
        delimiter,
        encoding,
        newline,
        quotechar,
        escapechar,
        strict_headers,
        expected_headers,
        on_mismatch,
        recurse,
        case_insensitive,
        include_hidden,
    )
