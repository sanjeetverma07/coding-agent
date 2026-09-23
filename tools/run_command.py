import subprocess
from utils.config import REPO_ROOT, ALLOWED_COMMANDS




def run_command(command: str) -> dict:

    # Exact command allow-list
    if command not in ALLOWED_COMMANDS:

        return {
            "success": False,
            "error": (
                f"Command not allowed: {command}. "
                f"Allowed commands: "
                f"{list(ALLOWED_COMMANDS)}"
            )
        }

    try:

        result = subprocess.run(
            command,
            shell=True,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout[-10_000:],
            "stderr": result.stderr[-10_000:]
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "error": "Command timed out after 30 seconds"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }