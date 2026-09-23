from utils.config import REPO_ROOT
from .safe_search import safe_path

def list_files(directory: str = ".") -> dict:
    """
    list all the present in the ROOT folder.
    """
    
    try:
        directory_path = safe_path(directory)

        if not directory_path.exists():
            return {
                "success": False,
                "error": "Directory does not exist"
            }

        if not directory_path.is_dir():
            return {
                "success": False,
                "error": "Path is not a directory"
            }

        files = []

        for path in directory_path.rglob("*"):
            if path.is_file():
                files.append(
                    str(path.relative_to(REPO_ROOT))
                )

        return {
            "success": True,
            "files": files
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

