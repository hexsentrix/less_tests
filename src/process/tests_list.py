"""
List tests that depend on a file.
tests are in json file in tests.json.
tests.json sample:
```
{
 "tests": [
  {
   "number": 0,
   "id": "tests/dialects/test_athena.py::TestAthena::test_athena",
   "file": "tests/dialects/test_athena.py",
   "seconds": 0.034
  },
  {
   "number": 1,
   "id": "tests/dialects/test_athena.py::TestAthena::test_create_table",
   "file": "tests/dialects/test_athena.py",
   "seconds": 0.002
  },
  {
   "number": 2,
   "id": "tests/dialects/test_athena.py::TestAthena::test_ctas",
   "file": "tests/dialects/test_athena.py",
   "seconds": 0.002
  }
 ]
}
```
"""
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Test:
    file: str
    number: int
    seconds: float
    id: str

def get_all_tests(tests_file: str = "tests.json")->list[Test]:
    with open(tests_file, "r", encoding="utf-8") as f:
        tests_data = json.load(f)
    dependent_tests = [
        Test(test["file"], test["number"], test["seconds"], test["id"])
        for test in tests_data.get("tests", [])
    ]
    
    return dependent_tests