from  ingestion.indexer import indexer

def search_repository(query: str, top_k: int = 5):
    try:
        results = indexer.search(
            query,
            top_k
        )
        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
        
def search_repository_hybrid(query: str, top_k: int = 5):
    try:
        results = indexer.hybrid_search(
            query=query,
            top_k=top_k
        )
        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }