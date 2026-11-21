from input.read_input import read_input
from process.process_data import process_data,CommitTests
from output.write_output import write_output
from os import listdir,getenv


def main():
    commits:list[CommitTests]=[]
    for commit in listdir("commits"):
        if commit.endswith('.patch'):
            commit_id = commit.split('.')[0]
            #print("=" * 40,commit_id,"=" * 40)
            data = read_input(commit_id)
            processed_data = process_data(commit_id, data)
            commits.append(processed_data)
    write_output(commits)
if __name__ == '__main__':
    main()
