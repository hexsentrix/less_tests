import unidiff
from pathlib import Path
from os import getenv


diff_files_root = Path("commits")
def read_diff(diff_file:Path)->unidiff.PatchSet:
    with open(diff_files_root / diff_file, "r", encoding="utf-8") as f:
        return unidiff.PatchSet.from_string(f.read())