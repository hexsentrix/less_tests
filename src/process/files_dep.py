import json
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent

def get_files_dep(dep_graph: str = PROJECT_ROOT/"assets/tests_deps.json",target='sqlglot', target_keyword='tests') -> dict[str:list[str]]:
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

    


if __name__ == "__main__":
    for i in get_files_dep().items():
        print(i)