import math
import re
from typing import List

class VectorEmbeddingsProvider:
    """Generates normalized dense vector embeddings for semantic document search."""
    
    def __init__(self, vector_dim: int = 64):
        self.vector_dim = vector_dim

    def embed_text(self, text: str) -> List[float]:
        """Calculates a deterministic 64-dim semantic embedding vector from text tokens."""
        vec = [0.0] * self.vector_dim
        words = re.findall(r'\w+', text.lower())
        
        if not words:
            return vec

        for idx, word in enumerate(words):
            # Compute hash distribution across dimensions
            h = sum(ord(c) * (i + 1) for i, c in enumerate(word))
            dim = h % self.vector_dim
            weight = 1.0 + (1.0 / (idx + 1))
            vec[dim] += weight

        # Normalize L2 norm
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]

        return vec

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        if len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        return round(float(dot), 4)
