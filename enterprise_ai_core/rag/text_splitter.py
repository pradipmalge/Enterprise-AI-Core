from typing import List
from .document_loader import Document

class RecursiveCharacterTextSplitter:
    """Enterprise Recursive Text Splitter for optimal vector chunking."""
    
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 50, separators: List[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks: List[Document] = []
        for doc in documents:
            doc_chunks = self.split_text(doc.content)
            for idx, text in enumerate(doc_chunks):
                meta = doc.metadata.copy()
                meta["chunk_index"] = idx
                meta["chunk_count"] = len(doc_chunks)
                chunks.append(Document(content=text, metadata=meta))
        return chunks

    def split_text(self, text: str) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text.strip()] if text.strip() else []

        # Find best separator
        separator = self.separators[-1]
        for s in self.separators:
            if s in text:
                separator = s
                break

        parts = text.split(separator) if separator else list(text)
        chunks = []
        current_chunk = ""

        for part in parts:
            candidate = current_chunk + (separator if current_chunk else "") + part
            if len(candidate) <= self.chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = part

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
