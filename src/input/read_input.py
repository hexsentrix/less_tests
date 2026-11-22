from .read_diff import read_diff
from pathlib import Path
from .edited_element import patch_set_to_edited_elements


def read_input(commit_id):
    diff = read_diff(Path(commit_id))
    data = patch_set_to_edited_elements(diff)
    return data

if __name__ == "__main__":
    from os import getenv
    from os import listdir
    from os.path import isfile, join
    commit_files = [f for f in listdir("commits")]
    print(f"Found {len(commit_files)} commit files.")
    for commit_file in commit_files:
        commit_id = commit_file.split('.')[0]
        print("=" * 40,commit_id,"=" * 40)
        data = read_input(commit_file)
        print(f"Commit ID: {commit_id}")
        print(f"Data: {data}")
