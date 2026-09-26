import subprocess


def run_git(command: list[str]) -> dict:
    """
    tool for running the git commands this takes command as parameter to execute
    """
    
    try:
        result = subprocess.run(
            ["git"] + command,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Git command timed out"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def git_status() -> dict:
    return run_git([
        "status",
        "--short"
    ])


def git_diff() -> dict:
    return run_git([
        "diff"
    ])


def git_log(limit: int = 10) -> dict:
    return run_git([
        "log",
        f"-{limit}",
        "--oneline"
    ])


def git_branch() -> dict:
    return run_git([
        "branch",
        "--show-current"
    ])

def git_stash() -> dict:
    return run_git([
        "stash"
    ])
    
def git_stash_pop() -> dict:
    return run_git([
        "stash _pop"
    ])
    
def git_create_branch(branch_name: str) -> dict:
    return run_git([
        "checkout",
        "-b",
        branch_name
    ])


def git_checkout(branch_name: str) -> dict:
    return run_git([
        "checkout",
        branch_name
    ])


def git_add(paths: list[str]) -> dict:
    return run_git([
        "add",
        "--",
        *paths
    ])


def git_commit(message: str) -> dict:
    return run_git([
        "commit",
        "-m",
        message
    ])