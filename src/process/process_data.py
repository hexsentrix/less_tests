from .tests_depenancies import get_tests_depenancies
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
    tests = get_all_tests()
    commit_tests = CommitTests(commit_id=commit_id, failing=[], kind="code")
    for test in tests:
        test_file = test.file
        for py_file in edited_files:
            if py_file.py_import_name in tests_depenancies[test_file]:
                commit_tests.failing.append(test)
    return commit_tests