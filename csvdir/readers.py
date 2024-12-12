from dataclasses import dataclass
import csv
import os
import typing


from csvdir import pathing as _pathing
from csvdir import chunking as _chunking
 
 
@dataclass
class IterEnumPathsCsvDir:
    path: str
    extension: str = 'csv'
    delimiter: str = ','
 
    def __post_init__(self) -> None:
        self.csv_file_paths = _pathing.get_csv_paths(self.path, self.extension)
        self.reader = self.dict_rows()
       
    def dict_rows(self) -> typing.Generator[tuple[int, str, dict], None, None]:
        for path in self.csv_file_paths:
            with open(path, 'r') as f:
                reader = csv.DictReader(f, delimiter=self.delimiter)
                for i, row in enumerate(reader):
                    yield i, path, row
           
    def __next__(self) -> tuple[int, str, dict]:
        return next(self.reader)
 
    def __iter__(self):
        return self
    

class IterPathsCsvDir(IterEnumPathsCsvDir):
    def dict_rows(self) -> typing.Generator[tuple[str, dict], None, None]:
        for _, full_path, row in IterEnumPathsCsvDir.dict_rows(self):
            yield full_path, row
           
    def __next__(self) -> tuple[str, dict]:
        return next(self.reader)
 
    def __iter__(self):
        return self
    
    def enumerate(self) -> IterEnumPathsCsvDir:
        return IterEnumPathsCsvDir(self.path, self.extension, self.delimiter)
    
 
class IterEnumNamesCsvDir(IterEnumPathsCsvDir):
    def dict_rows(self) -> typing.Generator[tuple[int, str, dict], None, None]:
        for i, full_path, row in IterEnumPathsCsvDir.dict_rows(self):
            yield i, _pathing.get_name(full_path), row


class IterNamesCsvDir(IterPathsCsvDir):
    def dict_rows(self) -> typing.Generator[tuple[str, dict], None, None]:
        for full_path, row in IterPathsCsvDir.dict_rows(self):
            yield _pathing.get_name(full_path), row

    def enumerate(self):
        return IterEnumNamesCsvDir(self.path, self.extension, self.delimiter)
 
 
class IterEnumCsvDir(IterEnumPathsCsvDir):
    def dict_rows(self) -> typing.Generator[tuple[int, dict], None, None]:
        for i, _, row in IterEnumPathsCsvDir.dict_rows(self):
            yield i, row
           
    def __next__(self) -> tuple[int, dict]:
        return next(self.reader)
 

class IterCsvDir(IterPathsCsvDir):
    def dict_rows(self) -> typing.Generator[dict, None, None]:
        for _, row in IterPathsCsvDir.dict_rows(self):
            yield row
           
    def __next__(self) -> dict:
        return next(self.reader)
    
    def enumerate(self) -> IterEnumCsvDir:
        return IterEnumCsvDir(self.path, self.extension, self.delimiter)
    
 
@dataclass
class CsvDir:
    path: str | None = None
    extension: str = 'csv'
    delimiter: str = ','
 
    def __post_init__(self) -> None:
        if self.path is None:
            self.path = os.getcwd()
    
    @property
    def paths(self):
        return _pathing.get_csv_paths(self.path, self.extension)
    
    @property
    def names(self):
        return [_pathing.get_name(path) for path in self.paths]

    def __iter__(self) -> IterCsvDir:
        return IterCsvDir(self.path, extension=self.extension, delimiter=self.delimiter)
 
    def with_names(self) -> IterNamesCsvDir:
        return IterNamesCsvDir(self.path, extension=self.extension, delimiter=self.delimiter)
 
    def with_paths(self) -> IterNamesCsvDir:
        return IterPathsCsvDir(self.path, extension=self.extension, delimiter=self.delimiter)
    
    def enumerate(self) -> IterEnumCsvDir:
        return IterEnumCsvDir(self.path, extension=self.extension, delimiter=self.delimiter)
    

def read_dir(
    path: str | None = None,
    extension: str = 'csv',
    delimiter: str = ',',
    *,
    chunksize: int | None = None
) -> CsvDir | _chunking.CsvChunksDir:
    if chunksize:
        return _chunking.CsvChunksDir(chunksize, path, extension, delimiter)
    return CsvDir(path, extension, delimiter)