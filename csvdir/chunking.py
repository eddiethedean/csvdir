"""
With chunking, chunks should only come from matching csv headers.
This will stop any strange mismatched column problems.

import csvdir


for chunk in csvdir.read_chunks('data/', 2):
    print(chunk)

[
    {'id': 1, 'name': 'Odos', 'age': 38},
    {'id': 2, 'name': 'Kayla', 'age': 31}
]
[
    {'id': 3, 'name': 'Dexter', 'age': 2}
]
[
    {'x': 55, 'y': 90},
    {'x': 90, 'y': 87}
]
"""
from collections import defaultdict
import os
import typing
from dataclasses import dataclass
import csv

from csvdir import pathing as _pathing


Row = dict[str, str]


class IndexesPathsChunk(typing.NamedTuple):
    indexes: list[int]
    paths: list[str]
    chunk: list[Row]


class IndexesNamesChunk(typing.NamedTuple):
    indexes: list[int]
    names: list[str]
    chunk: list[Row]


class PathsChunk(typing.NamedTuple):
    paths: list[str]
    chunk: list[Row]


class NamesChunk(typing.NamedTuple):
    names: list[str]
    chunk: list[Row]


class IndexesChunk(typing.NamedTuple):
    indexes: list[int]
    chunk: list[Row]
    

@dataclass
class IterEnumPathsCsvChunksDir:
    path: str
    chunksize: int
    extension: str = 'csv'
    delimiter: str = ','

    def __post_init__(self) -> None:
        self.csv_file_paths = _pathing.get_csv_paths(self.path, self.extension)
        self.reader = self.dict_rows()
        self.groups = group_by_columns(self.csv_file_paths, self.delimiter)

    def dict_rows(self) -> typing.Generator[IndexesPathsChunk, None, None]:
        for grouped_paths in self.groups.values():
            chunk = []
            paths = []
            indexes = []
            for path in grouped_paths:
                with open(path, 'r') as f:
                    reader = csv.DictReader(f, delimiter=self.delimiter)
                    for i, row in enumerate(reader):
                        chunk.append(row)
                        paths.append(path)
                        indexes.append(i)
                        if len(chunk) == self.chunksize:
                            yield IndexesPathsChunk(indexes, paths, chunk)
                            indexes = []
                            paths = []
                            chunk = []
            if chunk:
                yield IndexesPathsChunk(indexes, paths, chunk)
                indexes = []
                paths = []
                chunk = []
                
    def __next__(self) -> IndexesPathsChunk:
        return next(self.reader)

    def __iter__(self):
        return self


class IterPathsCsvChunksDir(IterEnumPathsCsvChunksDir):
    def dict_rows(self) -> typing.Generator[PathsChunk, None, None]:
        for _, paths, chunk in IterEnumPathsCsvChunksDir.dict_rows(self):
            yield PathsChunk(paths, chunk)
                
    def __next__(self) -> PathsChunk:
        return next(self.reader)

    def enumerate(self) -> IterEnumPathsCsvChunksDir:
        return IterEnumPathsCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)


class IterEnumNamesCsvChunksDir(IterEnumPathsCsvChunksDir):
    def dict_rows(self) -> typing.Generator[IndexesNamesChunk, None, None]:
        for indexes, paths, chunk in IterEnumPathsCsvChunksDir.dict_rows(self):
            yield IndexesNamesChunk(indexes, [_pathing.get_name(path) for path in paths], chunk)
                
    def __next__(self) -> IndexesNamesChunk:
        return next(self.reader)


class IterNamesCsvChunksDir(IterEnumNamesCsvChunksDir):
    def dict_rows(self) -> typing.Generator[NamesChunk, None, None]:
        for _, names, chunk in IterEnumNamesCsvChunksDir.dict_rows(self):
            yield NamesChunk(names, chunk)
                
    def __next__(self) -> NamesChunk:
        return next(self.reader)

    def enumerate(self) -> IterEnumNamesCsvChunksDir:
        return IterEnumNamesCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)


class IterEnumCsvChunksDir(IterEnumPathsCsvChunksDir):
    def dict_rows(self) -> typing.Generator[IndexesChunk, None, None]:
        for indexes, _, chunk in IterEnumPathsCsvChunksDir.dict_rows(self):
            yield IndexesChunk(indexes, chunk)
                
    def __next__(self) -> IndexesChunk:
        return next(self.reader)

    def with_paths(self) -> IterEnumPathsCsvChunksDir:
        return IterEnumPathsCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)

    def with_names(self) -> IterEnumNamesCsvChunksDir:
        return IterEnumNamesCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)


class IterCsvChunksDir(IterPathsCsvChunksDir):
    def dict_rows(self) -> typing.Generator[list[Row], None, None]:
        for _, chunk in IterPathsCsvChunksDir.dict_rows(self):
            yield chunk
                
    def __next__(self) -> list[Row]:
        return next(self.reader)

    def enumerate(self) -> IterEnumCsvChunksDir:
        return IterEnumCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)

    def with_paths(self) -> IterPathsCsvChunksDir:
        return IterPathsCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)

    def with_names(self) -> IterNamesCsvChunksDir:
        return IterNamesCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)


@dataclass
class CsvChunksDir:
    chunksize: int
    path: str | None = None
    extension: str = 'csv'
    delimiter: str = ','

    def __post_init__(self) -> None:
        if self.path is None:
            self.path = os.getcwd()

    def __iter__(self) -> IterCsvChunksDir:
        return IterCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)
 
    def with_names(self) -> IterNamesCsvChunksDir:
        return IterNamesCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)
 
    def with_paths(self) -> IterPathsCsvChunksDir:
        return IterPathsCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)
    
    def enumerate(self) -> IterEnumCsvChunksDir:
        return IterEnumCsvChunksDir(self.path, self.chunksize, self.extension, self.delimiter)


def read_dir_chunks(
    chunksize: int,
    path: str | None = None,
    extension: str = 'csv',
    delimiter: str = ','
) -> CsvChunksDir:
    return CsvChunksDir(chunksize, path, extension, delimiter)


def get_headers(path: str, delimiter: str) -> frozenset[str]:
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return frozenset(reader.fieldnames)
    

def group_by_columns(
    csv_file_paths: list[str],
    delimiter: str
) -> dict[frozenset[str], list[str]]:
    groups: dict[frozenset[str], list[str]] = defaultdict(list)
    for path in csv_file_paths:
        groups[get_headers(path, delimiter)].append(path)
    return {cols: sorted(groups[cols]) for cols in sorted(groups)}