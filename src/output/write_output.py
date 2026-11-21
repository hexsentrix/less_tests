"""
smaple json out put:
{
 "commits": {
  "2haz": {
   "failing": [],
   "kind": "code"
  },
  "2jrq": {
   "failing": [
    1104,
    1106,
    1325,
    1355,
    1369,
    1381,
    1440,
    1441
   ],
   "kind": "code"
  },
  "2qn5": {
   "failing": [],
   "kind": "code"
  },
  "2vdj": {
   "failing": [
    1377
   ],
   "kind": "fixture"
  },
  "st8f": {
   "failing": [
    1335
   ],
   "kind": "fixture"
  }
 }
}
"""
import json
from os import getenv

def commit_tests_to_dict(commit_tests):
    return {
            commit_tests.commit_id: {
                "failing": [fail.number for fail in commit_tests.failing],
                "kind": commit_tests.kind
            }
        }

def write_output_to_json(processed_data):#commits list to write to json file
    output_dict = {"commits": {}}
    for commit in processed_data:
        output_dict["commits"].update(commit_tests_to_dict(commit))
    with open(getenv("output_file_path", "output.json"), "w") as f:
        json.dump(output_dict, f)

def split_accross(tests , worker_count: int=3) -> list[list[int]]:
    """Longest test first, each onto the worker with the least to do so far."""
    workers: list[list[int]] = [[] for _ in range(worker_count)]
    loads = [0.0] * worker_count
    for test in sorted(tests, key=lambda test: test.seconds, reverse=True):
        lightest = loads.index(min(loads))
        workers[lightest].append(test.number)
        loads[lightest] += test.seconds
    return workers

def write_output(processed_data):
    for commit in processed_data:
        print(json.dumps({"commit": commit.commit_id, "workers": split_accross(commit.failing)}))