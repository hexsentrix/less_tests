from .files_dep import get_files_dep
from .dependent_list import get_dependent_tests,Test
from dataclasses import dataclass
from pathlib import Path
@dataclass
class CommitTests:
    commit_id: str
    failing: list[Test] #tests that may fail so we can rerun them
    kind: str # code | fixture

def class_tests(classes_names):
    dependents = get_dependent_tests()
    class_dependent=[]
    for class_name in classes_names:
        for dependent in dependents:
            dependent_file = dependent.file
            if class_name.lower_name in dependent_file.lower():
                class_dependent.append(dependent)
    return class_dependent

def process_data(commit_id, edited_files=None,additional_dep=None):# data: EditedElement for edited_element.py
    files_dep = get_files_dep()
    dependents = get_dependent_tests()
    commit_tests = CommitTests(commit_id=commit_id, failing=additional_dep, kind="code")
    for dependent in dependents:
        dependent_file = dependent.file
        if 'optimizer' in dependent_file:
            commit_tests.failing.append(dependent)
        if 'expr' in dependent_file:
            commit_tests.failing.append(dependent)
        for py_file in edited_files:
            if py_file.py_import_name in files_dep[dependent_file]:
                commit_tests.failing.append(dependent)
    return commit_tests