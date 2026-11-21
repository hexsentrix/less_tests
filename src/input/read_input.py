from .read_diff import read_diff
from pathlib import Path
from .edited_element import PatachSet_to_EditedElements
from .list_affected import list_affected


def read_input(commit_id):
    data = read_diff(Path(commit_id))
    data = PatachSet_to_EditedElements(data)
    return list_affected(data)

if __name__ == "__main__":
    from os import getenv
    from os import listdir
    from os.path import isfile, join
    commit_files = [f for f in listdir("commits") if isfile(join("commits", f)) and f.endswith(commit_ext)]
    print(f"Found {len(commit_files)} commit files.")
    for commit_file in commit_files:
        commit_id = commit_file.split('.')[0]
        print("=" * 40,commit_id,"=" * 40)
        data = read_input(commit_file)
        print(f"Commit ID: {commit_id}")
        print(f"Data: {data}")
