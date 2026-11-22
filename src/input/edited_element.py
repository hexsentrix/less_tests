
import ast
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from unidiff import PatchSet
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
COMMENT_DIRECTIVES = (
    "!",
    ":",
    "coding:",
    "coding=",
    "type:",
    "type=",
    "noqa",
    "nosec",
    "pragma:",
    "pylint:",
    "pyright:",
    "mypy:",
    "pytype:",
    "pyre-",
    "ruff:",
    "flake8:",
    "isort:",
    "coverage:",
    "fmt:",
    "doctest:",
    "pytest:",
    "cython:",
    "noinspection",
)

@dataclass
class EditedElement:
    file_path: str
    py_import_name: str | None = None
    has_executable_changes: bool = True

def is_python_file(file_path: str) -> bool:
    return Path(file_path).suffix == ".py"

def _parse_hunk_ast(source: str) -> ast.Module | None:
    try:
        return ast.parse(source, type_comments=True)
    except SyntaxError as error:
        if "unterminated triple-quoted string literal" not in error.msg:
            return None

    parsed = []
    for quote in ('"""', "'''"):
        try:
            parsed.append(ast.parse(f"{source}\n{quote}", type_comments=True))
        except SyntaxError:
            continue

    return parsed[0] if len(parsed) == 1 else None

def _has_comment_directive(line: str) -> bool:
    comment = line.split("#", 1)
    if len(comment) == 1:
        return False
    content = comment[1].lower().lstrip()
    return any(content.startswith(marker) for marker in COMMENT_DIRECTIVES)

def has_executable_changes(patched_file) -> bool:
    if patched_file.is_added_file or patched_file.is_removed_file or patched_file.is_rename:
        return True

    has_hunks = False
    for hunk in patched_file:
        has_hunks = True
        changed_lines = [
            line.value
            for line in hunk
            if line.is_added or line.is_removed
        ]
        if any(_has_comment_directive(line) for line in changed_lines):
            return True

        old_source = "".join(line.value for line in hunk if not line.is_added)
        new_source = "".join(line.value for line in hunk if not line.is_removed)
        old_ast = _parse_hunk_ast(old_source)
        new_ast = _parse_hunk_ast(new_source)
        if (
            old_ast is None
            or new_ast is None
            or not old_ast.body
            or not new_ast.body
            or ast.dump(old_ast, include_attributes=False)
            != ast.dump(new_ast, include_attributes=False)
        ):
            return True

    return not has_hunks

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
            py_import_name=(
                python_file_path_to_import_name(file_path, target_root=Path("."))
                if is_python_file(file_path)
                else None
            ),
            has_executable_changes=(
                has_executable_changes(patched_file)
                if is_python_file(file_path)
                else True
            ),
        )
        edited_elements.append(edited_element)
    return edited_elements