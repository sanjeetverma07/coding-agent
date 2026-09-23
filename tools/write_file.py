from .safe_search import safe_path

MAX_FILE_SIZE = 100000

def write_file(path: str, content: str) -> dict:

    try:

        file_path = safe_path(path)

        if len(content.encode("utf-8")) > MAX_FILE_SIZE:

            return {
                "success": False,
                "error": "File is too large"
            }

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "message": f"Successfully wrote {path}",
            "path": path
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

