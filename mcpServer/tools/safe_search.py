from pathlib import Path
from utils.config import REPO_ROOT

def safe_path( path: str) -> Path:
    """
    Convert a user/LLM supplied path into a safe repository path.
    Prevents ../ and absolute-path traversal.
    """

    requested = (REPO_ROOT / path).resolve()

    if not requested.is_relative_to(REPO_ROOT):
        raise ValueError("Access outside repository is not allowed.")

    return requested
