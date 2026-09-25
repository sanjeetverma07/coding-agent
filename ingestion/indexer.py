from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import json


REPO_ROOT = Path("./test_repo").resolve()

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}


class CodeIndexer:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
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

            if path.suffix not in {
                ".py",
                ".js",
                ".ts",
                ".tsx",
                ".java",
                ".go",
                ".jsx",
            }:
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