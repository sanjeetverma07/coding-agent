import subprocess
from pathlib import Path


class BenchmarkManager:

    def __init__(self, repo_path: str):

        self.repo = Path(repo_path).resolve()

        if not self.repo.is_dir():
            raise ValueError(
                f"Benchmark repository does not exist: {self.repo}"
            )

        if not (self.repo / ".git").exists():
            raise ValueError(
                f"Not a Git repository: {self.repo}"
            )

    def git(self, *args):

        result = subprocess.run(
            ["git", *args],
            cwd=str(self.repo),
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    def reset_to(self, ref="eval-baseline"):

        result = self.git(
            "reset",
            "--hard",
            ref
        )

        if not result["success"]:
            raise RuntimeError(
                f"Failed to reset repository to "
                f"'{ref}':\n{result['stderr']}"
            )

        result = self.git(
            "clean",
            "-fd"
        )

        if not result["success"]:
            raise RuntimeError(
                f"Failed to clean repository:\n"
                f"{result['stderr']}"
            )

    def status(self):

        return self.git(
            "status",
            "--short"
        )

    def current_commit(self):

        result = self.git(
            "rev-parse",
            "HEAD"
        )

        if not result["success"]:
            raise RuntimeError(
                result["stderr"]
            )

        return result["stdout"].strip()