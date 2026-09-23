from .safe_search import safe_path

def read_file( path: str) -> dict:
    """
    reads the content present in the file
    """
    
    try:
        file_path = safe_path(path)

        if not file_path.exists():
            return {
                "success": False,
                "error": "File does not exist"
            }

        if not file_path.is_file():
            return {
                "success": False,
                "error": "Path is not a file"
            }

        # Safety limit
        if file_path.stat().st_size > 100_000:
            return {
                "success": False,
                "error": "File is too large to read"
            }

        content = file_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        return {
            "success": True,
            "path": path,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
