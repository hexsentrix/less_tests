from input.read_input import read_input
from process.process_data import process_data,CommitTests
from output.write_output import write_output
from os import listdir,getenv


def main():
    commits:list[CommitTests]=[]
    for commit in listdir("commits"):
        commit_id = commit
        data = read_input(commit_id)
        processed_data = process_data(commit_id, data)
        commits.append(processed_data)
    write_output(commits)
if __name__ == '__main__':
    main()
