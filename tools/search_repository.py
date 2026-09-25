from  ingestion.indexer import CodeIndexer
indexer = CodeIndexer()
indexer.build()

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