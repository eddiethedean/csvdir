import csvdir
import pytest


def test_strict_headers_uses_first_file_as_canonical(tmp_path, write_csv):
    write_csv("a.csv", ["id", "name", "age"], [["1", "a", "9"]])
    write_csv("b.csv", ["id", "name", "age"], [["2", "b", "10"]])
    r = csvdir.read_dir(str(tmp_path), strict_headers=True)
    assert len(list(r)) == 2  # no errors


def test_expected_headers_error_on_mismatch(tmp_path, write_csv):
    write_csv("a.csv", ["id", "name", "age"], [["1", "a", "9"]])
    write_csv("b.csv", ["id", "name"], [["2", "b"]])
    r = csvdir.read_dir(str(tmp_path), expected_headers=["id", "name", "age"], on_mismatch="error")
    with pytest.raises(ValueError):
        list(r)  # mismatch should raise


def test_expected_headers_skip_on_mismatch(tmp_path, write_csv):
    write_csv("a.csv", ["id", "name", "age"], [["1", "a", "9"]])
    write_csv("b.csv", ["id", "name"], [["2", "b"]])
    r = csvdir.read_dir(str(tmp_path), expected_headers=["id", "name", "age"], on_mismatch="skip")
    rows = list(r)
    # only rows from a.csv should be counted
    assert len(rows) == 1


def test_set_based_headers_allow_column_reorder_across_files(tmp_path, write_csv):
    """CsvDir matches column *names* as a set; permuted header rows still match."""
    write_csv("aaa_first.csv", ["id", "name"], [["1", "A"]])
    write_csv("zzz_second.csv", ["name", "id"], [["B", "2"]])
    r = csvdir.read_dir(str(tmp_path))
    assert len(list(r)) == 2


def test_csvdirfile_sequence_headers_skip_reordered_file(tmp_path, write_csv):
    """CsvDirFile requires header *sequence* to match the canonical first file."""
    from csvdir import CsvDirFile

    write_csv("aaa_first.csv", ["id", "name"], [["1", "A"]])
    write_csv("zzz_second.csv", ["name", "id"], [["B", "2"]])
    f = CsvDirFile(str(tmp_path), strict_headers=True, on_mismatch="skip")
    lines = list(f)
    assert len(lines) == 2  # header + single data row from first file only
    assert lines[0].strip() == "id,name"
