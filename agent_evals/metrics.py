import json
import subprocess
import time
from pathlib import Path

from benchmark import BenchmarkManager


class EvaluationRunner:

    def __init__(
        self,
        repo_path: str,
        cases_path: str
    ):
        self.repo_path = Path(repo_path).resolve()
        self.cases_path = Path(cases_path).resolve()

        self.benchmark = BenchmarkManager(
            str(self.repo_path)
        )

        with open(
            self.cases_path,
            "r",
            encoding="utf-8"
        ) as f:
            self.cases = json.load(f)

    def get_case(self, case_id):

        for case in self.cases:

            if case["id"] == case_id:
                return case

        raise ValueError(
            f"Evaluation case not found: {case_id}"
        )

    def run_tests(self, tests):

        results = []

        for command in tests:

            start = time.perf_counter()

            result = subprocess.run(
                command,
                cwd=str(self.repo_path),
                shell=True,
                capture_output=True,
                text=True
            )

            duration = time.perf_counter() - start

            results.append({
                "command": command,
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration_seconds": duration
            })

        return results

    def get_changed_files(self):

        result = self.benchmark.git(
            "diff",
            "--name-only"
        )

        if not result["success"]:
            raise RuntimeError(
                result["stderr"]
            )

        files = [
            line.strip()
            for line in result["stdout"].splitlines()
            if line.strip()
        ]

        return files

    def run_case(self, case_id):

        case = self.get_case(case_id)

        print("\n" + "=" * 60)
        print(f"EVALUATION: {case['id']}")
        print("=" * 60)

        print("\nTask:")
        print(case["task"])

        base_ref = case.get(
            "base_ref",
            "eval-baseline"
        )

        print(
            f"\nResetting repository to: {base_ref}"
        )

        self.benchmark.reset_to(base_ref)

        start_time = time.perf_counter()

        try:

            print("\nStarting agent...")

            # Agent execution will be connected here
            agent_result = None

            print("\nRunning tests...")

            test_results = self.run_tests(
                case.get("tests", [])
            )

            changed_files = self.get_changed_files()

            duration = (
                time.perf_counter()
                - start_time
            )

            tests_passed = all(
                result["success"]
                for result in test_results
            )

            expected_files = set(
                case.get("expected_files", [])
            )

            changed_set = set(
                changed_files
            )

            expected_files_changed = (
                expected_files
                .issubset(changed_set)
            )

            success = (
                tests_passed
                and expected_files_changed
            )

            result = {
                "case_id": case["id"],
                "category": case["category"],
                "success": success,
                "duration_seconds": duration,
                "changed_files": changed_files,
                "expected_files": list(
                    expected_files
                ),
                "expected_files_changed":
                    expected_files_changed,
                "tests": test_results,
                "agent_result": agent_result
            }

            return result

        finally:

            print(
                "\nResetting repository "
                "after evaluation..."
            )

            self.benchmark.reset_to(
                "eval-baseline"
            )