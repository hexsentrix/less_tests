
#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_result(data):
    """
    Expected result format:
    [
        {"commit": "2haz", "workers": [[1, 2], [3]]},
        ...
    ]
    """
    results = {}

    # Also support {"commits": {...}} if needed.
    if isinstance(data, dict) and "commits" in data:
        return {
            commit: set(info.get("failing", []))
            for commit, info in data["commits"].items()
        }

    if isinstance(data, list):
        lines = data
    else:
        raise ValueError("Unsupported result.json format")

    for item in lines:
        commit = item["commit"]
        tests = {
            test
            for worker in item["workers"]
            for test in worker
        }

        if commit in results:
            raise ValueError(f"Duplicate commit: {commit}")

        results[commit] = tests

    return results


def extract_solution(data):
    return {
        commit: set(info.get("failing", []))
        for commit, info in data["commits"].items()
    }


def calculate_metrics(tp, fp, fn, tn):
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )
    accuracy = (
        (tp + tn) / (tp + fp + fn + tn)
        if tp + fp + fn + tn else 0
    )

    return precision, recall, f1, accuracy


def compare(result, solution, verbose=True):
    common_commits = result.keys() & solution.keys()

    missing_commits = solution.keys() - result.keys()
    unknown_commits = result.keys() - solution.keys()

    totals = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}

    print("=" * 75)
    print("RWX TEST SELECTION COMPARISON")
    print("=" * 75)

    for commit in sorted(common_commits):
        predicted = result[commit]
        actual = solution[commit]

        tp = len(predicted & actual)
        fp = len(predicted - actual)
        fn = len(actual - predicted)

        # TN requires knowing the complete test universe.
        tn = 0

        totals["TP"] += tp
        totals["FP"] += fp
        totals["FN"] += fn

        precision, recall, f1, _ = calculate_metrics(
            tp, fp, fn, tn
        )

        missed = sorted(actual - predicted)
        unnecessary = sorted(predicted - actual)

        print(f"\nCommit: {commit}")
        print(f"  Actual failing : {len(actual)}")
        print(f"  Predicted      : {len(predicted)}")
        print(f"  TP             : {tp}")
        print(f"  FP             : {fp}")
        print(f"  FN             : {fn}")
        print(f"  Precision      : {precision:.2%}")
        print(f"  Recall         : {recall:.2%}")
        print(f"  F1             : {f1:.2%}")

        if verbose:
            if missed:
                print(f"  MISSED tests   : {missed}")
            if unnecessary:
                print(f"  Extra tests    : {unnecessary}")

    precision, recall, f1, _ = calculate_metrics(
        totals["TP"],
        totals["FP"],
        totals["FN"],
        totals["TN"],
    )

    print("\n" + "=" * 75)
    print("OVERALL")
    print("=" * 75)

    print(f"Compared commits : {len(common_commits)}")
    print(f"Missing commits  : {len(missing_commits)}")
    print(f"Unknown commits  : {len(unknown_commits)}")
    print(f"TP               : {totals['TP']}")
    print(f"FP               : {totals['FP']}")
    print(f"FN               : {totals['FN']}")
    print(f"Precision        : {precision:.2%}")
    print(f"Recall           : {recall:.2%}")
    print(f"F1-score         : {f1:.2%}")

    if missing_commits:
        print(f"\nMissing commits: {sorted(missing_commits)}")

    if unknown_commits:
        print(f"\nUnknown commits: {sorted(unknown_commits)}")

    commits_with_misses = [
        commit for commit in common_commits
        if solution[commit] - result[commit]
    ]

    print(f"\nCommits with missed tests: {len(commits_with_misses)}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare RWX test selection with ground truth."
    )

    parser.add_argument("result", type=Path)
    parser.add_argument("solution", type=Path)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide individual missed and extra test IDs."
    )

    args = parser.parse_args()

    result_data = load_json(args.result)
    solution_data = load_json(args.solution)

    result = extract_result(result_data)
    solution = extract_solution(solution_data)

    compare(result, solution, verbose=not args.quiet)


if __name__ == "__main__":
    main()
