import unidiff
from pathlib import Path
from os import getenv
from .edited_element import diff_file_to_AffectedClass,AffectedClass

diff_files_root = Path("commits")
def read_diff(diff_file:Path)->tuple[unidiff.PatchSet,AffectedClass|None]:
    with open(diff_files_root / diff_file, "r", encoding="utf-8") as f:
        text=f.read()
        if "class " in text:class_name = diff_file_to_AffectedClass(text)
        else: class_name = []
        return unidiff.PatchSet.from_string(text), class_name