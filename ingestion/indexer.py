from sentence_transformers import SentenceTransformer
import faiss
from utils.config import REPO_ROOT, IGNORE_DIRS, ACCEPTED_FILE_SUFFIX

class CodeIndexer:
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            cache_folder='/transformer_model'
        )
        self.documents = []
        self.index = None

    def get_files(self):
        files = []
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(
                part in IGNORE_DIRS
                for part in path.parts
            ):
                continue
            if path.suffix not in ACCEPTED_FILE_SUFFIX:
                continue
            files.append(path)
        return files

    def chunk_file(self, path):
        content = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
        lines = content.splitlines()
        chunk_size = 40
        chunks = []
        for i in range(0, len(lines), chunk_size):
            chunk = "\n".join(
                lines[i:i + chunk_size]
            )
            if chunk.strip():
                chunks.append({
                    "path": str(
                        path.relative_to(REPO_ROOT)
                    ),
                    "start_line": i + 1,
                    "end_line": min(
                        i + chunk_size,
                        len(lines)
                    ),
                    "content": chunk
                })
        return chunks
    
    # def build(self):
    #     self.documents = []
    #     for file in self.get_files():
    #         chunks = self.chunk_file(file)
    #         self.documents.extend(chunks)
    #         self.rebuild_index()
    #         print(
    #             f"Indexed {len(self.documents)} chunks"
    #         )
    def build(self):
        self.documents = []
        for file in self.get_files():
            chunks = self.chunk_file(file)
            self.documents.extend(chunks)
        texts = [
            doc["content"]
            for doc in self.documents
        ]
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(
            dimension
        )
        self.index.add(embeddings)
        print(
            f"Indexed {len(self.documents)} chunks"
        )

    def search(self, query, top_k=5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )
        distances, indices = self.index.search(
            query_embedding,
            top_k
        )
        results = []
        for distance, index in zip(
            distances[0],
            indices[0]
        ):
            if index == -1:
                continue
            document = self.documents[index]
            results.append({
                "path": document["path"],
                "start_line": document["start_line"],
                "end_line": document["end_line"],
                "content": document["content"],
                "distance": float(distance)
            })
        return results
    
    def update_file(self, path):
        """
        Re-index a single changed file.
        """
        file_path = REPO_ROOT / path
        # Remove existing chunks belonging to this file
        self.documents = [
            doc
            for doc in self.documents
            if doc["path"] != path
        ]

        # If file was deleted, we're done
        if not file_path.exists():
            self.rebuild_index()
            return

        # Create new chunks
        chunks = self.chunk_file(file_path)
        self.documents.extend(chunks)
        # Rebuild FAISS index from current documents
        self.rebuild_index()
        
        
    def rebuild_index(self):
        texts = [
            doc["content"]
            for doc in self.documents
        ]
        if not texts:
            self.index = None
            return
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(embeddings)
        
    def exact_search(self, query, top_k=5):
        """
        Search for exact text, function names, or class names
        in indexed repository chunks.
        """

        query_lower = query.lower().strip()
        if not query_lower:
            return []
        results = []
        for document in self.documents:
            content = document["content"].lower()
            name = (document.get("name") or "").lower()
            score = 0
            # Exact symbol match
            if name == query_lower:
                score += 100

            # Symbol contains query
            elif query_lower in name:
                score += 80
            # Exact text appears in code
            if query_lower in content:
                score += 50
            if score > 0:
                results.append({
                    "path": document["path"],
                    "start_line": document["start_line"],
                    "end_line": document["end_line"],
                    "type": document.get("type"),
                    "name": document.get("name"),
                    "content": document["content"],
                    "score": score
                })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]
    
    def hybrid_search(self, query, top_k=5):
        semantic_results = self.search(
            query=query,
            top_k=top_k
        )
        exact_results = self.exact_search(
            query=query,
            top_k=top_k
        )
        merged = {}
        # Add semantic results
        for result in semantic_results:
            key = (
                result["path"],
                result["start_line"],
                result["end_line"]
            )

            merged[key] = {
                **result,
                "search_type": "semantic"
            }

        # Add exact results
        for result in exact_results:
            key = (
                result["path"],
                result["start_line"],
                result["end_line"]
            )
            if key in merged:
                merged[key]["search_type"] = "hybrid"
                merged[key]["exact_score"] = result["score"]
            else:
                merged[key] = {
                    **result,
                    "search_type": "exact",
                    "distance": None,
                    "exact_score": result["score"]
                }

        results = list(merged.values())

        # Exact/hybrid matches get priority
        results.sort(
            key=lambda x: (
                x.get("exact_score", 0),
                -(
                    x.get("distance")
                    if x.get("distance") is not None
                    else 999999
                )
            ),
            reverse=True
        )
        return results[:top_k]
        
indexer = CodeIndexer()
indexer.build()