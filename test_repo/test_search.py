from ingestion.indexer import CodeIndexer
indexer = CodeIndexer()
indexer.build()

results = indexer.search(
    "authentication user token",
    top_k=5
)

for result in results:
    print("\n==============================")
    print(
        f"{result['path']}:"
        f"{result['start_line']}-"
        f"{result['end_line']}"
    )

    print(result["content"])