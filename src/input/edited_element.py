from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from unidiff import PatchSet


class ElementType(Enum):
    FILE = "file"
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    IMPORT = "import"
    UNKNOWN = "unknown"


class EditEffect(Enum):
    UNKNOWN = ("unknown", None)
    COMMENT = ("comment", False)
    PARG_TO_KEYWORD_ARG = ("parg_to_keyword_arg", None)
    ADD_OPTIONAL_ARG = ("add_optional_arg", None)
    EDIT_OPERATOR = ("edit_operator", True)
    FILE_RENAME = ("file_rename", True)
    FILE_REMOVE_OR_MOVE = ("file_remove_or_move", True)
    NEW_FILE = ("new_file", True)

    def __init__(self, label, affects_tests):
        self.label = label
        self.affects_tests = affects_tests


class ChangeType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"

@dataclass
class AffectedClass:
    name: str
    lower_name: str
    def __init__(self,name:str):
        self.name=name
        self.lower_name=name.lower()

@dataclass
class EditedElement:
    file_path: str
    change_type: ChangeType

    element_type: ElementType = ElementType.UNKNOWN
    py_import_name: str | None = None

    edit_effect: EditEffect = EditEffect.UNKNOWN
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

def PatachSet_to_EditedElements(patch_set: PatchSet) -> list[EditedElement]:
    edited_elements = []
    for patched_file in patch_set:
        file_path = patched_file.path
        if not is_python_file(Path(file_path)):
            assert file_path.endswith('.sql')
        change_type = ChangeType.ADDED if patched_file.is_added_file else ChangeType.REMOVED if patched_file.is_removed_file else ChangeType.MODIFIED

        edited_element = EditedElement(
            file_path=file_path,
            change_type=change_type,
            py_import_name=python_file_path_to_import_name(file_path, target_root=Path(".")),
        )
        edited_elements.append(edited_element)

    return edited_elements

def diff_file_to_AffectedClass(text: Path) -> list[AffectedClass]:
    class_name_start = text[text.index('class')+6:text.index('class')+12]
    class_name_end = text[text.index('(')-6:text.index('(')]
    return [AffectedClass(class_name_start),AffectedClass(class_name_end)]