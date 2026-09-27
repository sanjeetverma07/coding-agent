import json
import subprocess
import time
from pathlib import Path
import json
import subprocess
import time
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parent.parent / "agent"

if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))


from agent.agent import run_agent

from .benchmark import BenchmarkManager

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
            if command.strip().startswith("pytest"):
                command = f"python -m {command}"
            
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
    
    def run_eval_tests(self, eval_tests):
        results = []

        eval_root = self.cases_path.parent.parent / "eval_tests"

        for test_file in eval_tests:

            test_path = eval_root / Path(test_file).relative_to(
                "eval_tests"
            )

            command = f'python -m pytest "{test_path}"'

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
                "type": "evaluation",
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

    async def run_case(self, case_id):

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
            agent_result = await run_agent(case["task"])

            print("\nRunning tests...")

            test_results = self.run_tests(
                case.get("tests", [])
            )

            eval_test_results = self.run_eval_tests(
                case.get("eval_tests", [])
            )
            all_tests = [
                *test_results,
                *eval_test_results
            ]
            changed_files = self.get_changed_files()

            duration = (
                time.perf_counter()
                - start_time
            )

            tests_passed = all(
            result["success"]
                for result in all_tests
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
            
    def save_result(self, result):
        results_dir = (
            self.cases_path.parent.parent / "results"
        )

        results_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        result_path = results_dir / f"{result['case_id']}.json"

        with open(
            result_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                result,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"\nResult saved to: {result_path}")