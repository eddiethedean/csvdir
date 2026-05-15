import csvdir
import pytest
from csvdir import read_dir
from csvdir.chunks_dir import CsvChunksDir
from csvdir.dir_reader import CsvDir


def test_read_dir_factory_returns_correct_type(tmp_path, write_csv):
    write_csv("a.csv", ["h"], [["1"]])

    r = read_dir(str(tmp_path))
    assert isinstance(r, CsvDir)

    rc = csvdir.read_dir(str(tmp_path), chunksize=2)
    assert isinstance(rc, CsvChunksDir)


@pytest.mark.parametrize("bad", [-1, 0])
def test_read_dir_chunksize_must_be_positive(tmp_path, bad):
    with pytest.raises(ValueError, match="chunksize must be a positive"):
        csvdir.read_dir(str(tmp_path), chunksize=bad)


def test_read_dir_chunks_factory_validates_chunksize(tmp_path):
    with pytest.raises(ValueError, match="chunksize must be a positive"):
        csvdir.read_dir_chunks(str(tmp_path), chunksize=0)
