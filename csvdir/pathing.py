import glob
import os


def get_name(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def get_csv_paths(path: str, extension: str) -> list[str]:
    return sorted(glob.glob(os.path.join(path, f'*.{extension}')))