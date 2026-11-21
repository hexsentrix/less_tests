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
                "failing": commit_tests.failing,
                "kind": commit_tests.kind
            }
        }

def write_output(processed_data):#commits list to write to json file
    output_dict = {"commits": {}}
    for commit in processed_data:
        output_dict["commits"].update(commit_tests_to_dict(commit))
    with open(getenv("output_file_path", "output.json"), "w") as f:
        json.dump(output_dict, f)