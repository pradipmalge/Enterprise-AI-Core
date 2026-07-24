# RAG & Vector Search Module (`enterprise_ai_core.rag`)

The **RAG & Vector Search Module** extracts document text (PDFs, Markdown, JSON, HTML) and performs semantic vector embedding search.

## Document Extraction (`DocumentExtractor`)
Parses incoming documents into clean text chunks with chunking strategies.

## Vector Store (`InMemoryVectorStore`)
Stores vector embeddings and computes cosine similarity scores for retrieval augmented generation (RAG).

```python
from enterprise_ai_core.rag import DocumentExtractor, InMemoryVectorStore

store = InMemoryVectorStore()
await store.add_document("doc-1", "Enterprise SLA guarantee is 99.9% uptime.")
results = await store.similarity_search("What is the SLA uptime?", top_k=2)
```
