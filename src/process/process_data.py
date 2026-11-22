from .tests_depenancies import get_tests_depenancies, get_tests_fixture_dependencies
from .tests_list import get_all_tests,Test
from dataclasses import dataclass
from pathlib import Path
import os
@dataclass
class CommitTests:
    commit_id: str
    failing: list[Test] #tests that may fail so we can rerun them
    kind: str # code | fixture



def process_data(commit_id, edited_files=None):# data: EditedElement for edited_element.py
    tests_depenancies = get_tests_depenancies()
    tests_fixture_dependencies = get_tests_fixture_dependencies()
    tests = get_all_tests()
    has_python_code_changes = any(
        edited_file.py_import_name and edited_file.has_executable_changes
        for edited_file in edited_files
    )
    commit_tests = CommitTests(commit_id=commit_id, failing=[], kind="code")
    for test in tests:
        test_file = test.file
        if any(
            (
                has_python_code_changes
                and edited_file.py_import_name
                and edited_file.py_import_name in tests_depenancies[test_file]
            )
            or test.id
            in tests_fixture_dependencies.get(edited_file.file_path, [])
            for edited_file in edited_files
        ):
            commit_tests.failing.append(test)
    return commit_tests