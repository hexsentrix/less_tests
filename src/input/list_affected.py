from collections import deque
from dataclasses import dataclass
import json
from pathlib import Path

from .edited_element import EditedElement


@dataclass(frozen=True)
class Affected:
    py_import_name: str


def list_affected(
    edited_elements: list[EditedElement],
    code_deps_graph: Path = (
        Path(__file__).parent.parent.parent / "assets" / "code_deps.json"
    )
) -> list[Affected]:
    with open(code_deps_graph, "r", encoding="utf-8") as f:
        graph: dict = json.load(f)

    # Keep only elements with a valid Python import name.
    initial_imports = {
        element.py_import_name
        for element in edited_elements
        if element.py_import_name is not None
    }

    # BFS initialization.
    visited: set[str] = set(initial_imports)
    to_visit = deque(initial_imports)

    affected_files: list[Affected] = [
        Affected(name) for name in initial_imports
    ]

    while to_visit:
        current_module = to_visit.popleft()

        module_data = graph.get(current_module, {})
        imported_by = module_data.get("imported_by", [])

        for dependent in imported_by:
            if dependent in visited:
                continue

            # Mark visited when enqueuing, not when processing.
            visited.add(dependent)

            to_visit.append(dependent)
            affected_files.append(Affected(dependent))

    return affected_files
