import json
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent

def expand(files_dep:dict[str:list[str]])->dict[str:list[str]]:
    return files_dep

def get_tests_depenancies(dep_graph: str = PROJECT_ROOT/"assets/tests_deps.json",target='sqlglot', target_keyword='tests') -> dict[str:list[str]]:
    "Get The files that the py files depenace on"
    with open(dep_graph, "r", encoding="utf-8") as f:
        files = json.load(f)

    return {
        module_name.replace(".","/")+".py": list(
            filter(
                lambda imported_file: imported_file.startswith(target),
                data.get("imports", [])
                )
            )
        for module_name, data in files.items()
        }

def get_tests_fixture_dependencies(
    dep_graph: str = PROJECT_ROOT / "assets/fixtures_deps.json",
) -> dict[str, list[str]]:
    with open(dep_graph, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    for i in get_tests_depenancies().items():
        print(i)