from utils.config import REPO_ROOT

def search_code(query: str) -> dict:

    try:

        if not query:
            return {
                "success": False,
                "error": "Query cannot be empty"
            }

        results = []

        ignored = {
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "node_modules"
        }

        for path in REPO_ROOT.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in ignored
                for part in path.parts
            ):
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            except Exception:
                continue

            lines = content.splitlines()

            for line_number, line in enumerate(
                lines,
                start=1
            ):

                if query.lower() in line.lower():

                    results.append({
                        "file": str(
                            path.relative_to(REPO_ROOT)
                        ),
                        "line": line_number,
                        "content": line.strip()
                    })

                    # Prevent huge tool responses
                    if len(results) >= 100:

                        return {
                            "success": True,
                            "query": query,
                            "total_returned": len(results),
                            "truncated": True,
                            "matches": results
                        }

        return {
            "success": True,
            "query": query,
            "total_returned": len(results),
            "truncated": False,
            "matches": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


'''
def search_code( query: str) -> dict:
    """
    look for the code present in the file w.r.t user query
    """
    
    try:

        if not query:
            return {
                "success": False,
                "error": "Search query cannot be empty"
            }

        results = []

        for path in REPO_ROOT.rglob("*"):

            if not path.is_file():
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            except Exception:
                continue

            for line_number, line in enumerate(
                content.splitlines(),
                start=1
            ):

                if query.lower() in line.lower():

                    results.append({
                        "file": str(
                            path.relative_to(REPO_ROOT)
                        ),
                        "line": line_number,
                        "content": line.strip()
                    })

        return {
            "success": True,
            "query": query,
            "matches": results[:100]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
        
        '''