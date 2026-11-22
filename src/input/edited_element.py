
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from unidiff import PatchSet
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent

@dataclass
class EditedElement:
    file_path: str
    py_import_name: str | None = None

def is_python_file(file_path: str) -> bool:
    return Path(file_path).suffix == ".py"
def python_file_path_to_import_name(file_path: str, target_root: Path) -> str:
    """
    Convert a Python file path to its corresponding import name.
    For example, "src/utils/helpers.py" becomes "src.utils.helpers".
    """
    relative_path = Path(file_path).relative_to(target_root)
    import_name = ".".join(relative_path.with_suffix("").parts)
    return import_name

def patch_set_to_edited_elements(patch_set: PatchSet, dep_graph: str = PROJECT_ROOT/"assets/code_deps.json") -> list[EditedElement]:
    edited_elements = []
    with open(dep_graph, "r", encoding="utf-8") as f:
        files = json.load(f)
    for patched_file in patch_set:
        file_path = patched_file.path
        edited_element = EditedElement(
            file_path=file_path,
            py_import_name=python_file_path_to_import_name(file_path, target_root=Path(".")),
        )
        edited_elements.append(edited_element)
    return edited_elements