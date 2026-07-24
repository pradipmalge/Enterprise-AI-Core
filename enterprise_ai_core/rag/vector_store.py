from typing import List, Dict, Any, Tuple
from .document_loader import Document
from .embeddings import VectorEmbeddingsProvider

class VectorStore:
    """Enterprise In-Memory Vector Store for document index and top-K similarity search."""
    
    def __init__(self, embedder: VectorEmbeddingsProvider = None):
        self.embedder = embedder or VectorEmbeddingsProvider()
        self.index: List[Dict[str, Any]] = []

    def add_documents(self, docs: List[Document]) -> int:
        added = 0
        for doc in docs:
            embedding = self.embedder.embed_text(doc.content)
            self.index.append({
                "content": doc.content,
                "metadata": doc.metadata,
                "embedding": embedding,
                "id": f"chunk-{len(self.index) + 1}"
            })
            added += 1
        return added

    def similarity_search(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        if not self.index:
            return []

        query_vec = self.embedder.embed_text(query)
        scored: List[Tuple[Dict[str, Any], float]] = []

        for item in self.index:
            sim = VectorEmbeddingsProvider.cosine_similarity(query_vec, item["embedding"])
            scored.append((item, sim))

        # Sort descending by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for item, score in scored[:top_k]:
            doc = Document(content=item["content"], metadata=item["metadata"])
            results.append((doc, score))

        return results

    def clear(self):
        self.index.clear()
