from .safe_search import safe_path
from  ingestion.indexer import indexer

def replace_in_file(
    path: str,
    old: str,
    new: str
) -> dict:

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return {
                "success": False,
                "error": "File does not exist"
            }

        content = file_path.read_text(
            encoding="utf-8"
        )

        occurrences = content.count(old)
        if occurrences == 0:
            return {
                "success": False,
                "error": "Target text was not found"
            }
        if occurrences > 1:
            return {
                "success": False,
                "error": (
                    f"Target text appears {occurrences} times. "
                    "Refusing to make an ambiguous replacement."
                )
            }
        updated_content = content.replace(
            old,
            new,
            1
        )
        file_path.write_text(
            updated_content,
            encoding="utf-8"
        )
        indexer.update_file(path)
        return {
            "success": True,
            "path": path,
            "message": "File updated successfully"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }