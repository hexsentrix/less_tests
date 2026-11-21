from .files_dep import get_files_dep
from .dependent_list import get_dependent_tests,Test
from dataclasses import dataclass

@dataclass
class CommitTests:
    commit_id: str
    failing: list[Test] #tests that may fail so we can rerun them
    kind: str # code | fixture

def process_data(commit_id, data=None):# data: EditedElement for edited_element.py
    files_dep = get_files_dep()
    dependents = get_dependent_tests()
    commit_tests = CommitTests(commit_id=commit_id, failing=[], kind="code")
    for dependent in dependents:
        dependent_file = dependent.file
        for py_file in data:
            if py_file.py_import_name in files_dep[dependent_file]:
                commit_tests.failing.append(dependent)
        if 'sqlglotc' in files_dep[dependent_file]:
            commit_tests.kind = "fixture"
            commit_tests.failing.append(dependent.number)
    return commit_tests