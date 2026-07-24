import json
import re
from typing import Dict, Any, List
from enterprise_ai_core.tools import tool
from .document_loader import DocumentLoader, Document
from .text_splitter import RecursiveCharacterTextSplitter
from .vector_store import VectorStore

# Global RAG Instance for Agent Tool Calling
_GLOBAL_VECTOR_STORE = VectorStore()

@tool(
    name="extract_document_details",
    description="Extracts structured key details, clauses, financial figures, dates, and SLA metrics from raw document text."
)
def extract_document_details(document_text: str) -> str:
    """Extracts entity metadata and key terms from a document string."""
    dates = re.findall(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b', document_text, re.IGNORECASE)
    financials = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d+)?|\b\d+\s*(?:USD|EUR|GBP|million|billion)\b', document_text, re.IGNORECASE)
    percentages = re.findall(r'\b\d+(?:\.\d+)?%\b', document_text)
    
    # Extract candidate clauses or key sentences
    lines = [line.strip() for line in document_text.split('\n') if line.strip()]
    sections = [line for line in lines if len(line) < 60 and (line.endswith(':') or line.isupper() or line.startswith('#'))]

    extracted = {
        "document_summary": lines[0] if lines else "Empty document",
        "key_sections": sections[:5],
        "extracted_dates": list(set(dates)),
        "financial_terms": list(set(financials)),
        "metrics_sla": list(set(percentages)),
        "total_word_count": len(document_text.split()),
        "status": "EXTRACTED_SUCCESSFULLY"
    }
    return json.dumps(extracted, indent=2)

@tool(
    name="search_knowledge_base",
    description="Performs semantic vector search over ingested knowledge base chunks and returns top matching document citations."
)
def search_knowledge_base(query: str) -> str:
    """Performs cosine vector search across indexed knowledge base chunks."""
    results = _GLOBAL_VECTOR_STORE.similarity_search(query, top_k=3)
    if not results:
        return json.dumps({"query": query, "matches": [], "message": "No indexed document chunks found in Knowledge Base."})

    matches = []
    for doc, score in results:
        matches.append({
            "content": doc.content,
            "similarity_score": score,
            "source": doc.metadata.get("source", "knowledge_base"),
            "chunk_index": doc.metadata.get("chunk_index", 0)
        })

    return json.dumps({"query": query, "total_matches": len(matches), "matches": matches}, indent=2)

@tool(
    name="ingest_document_to_rag",
    description="Loads a raw document, chunks it into vector embeddings, and indexes it into the Enterprise RAG Knowledge Base."
)
def ingest_document_to_rag(document_text: str, source_name: str = "document.txt") -> str:
    """Ingests and indexes document into vector store."""
    loader = DocumentLoader()
    doc = loader.load_from_text(document_text, source_name=source_name)
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents([doc])
    
    added_count = _GLOBAL_VECTOR_STORE.add_documents(chunks)
    return json.dumps({
        "status": "INGESTED_AND_INDEXED",
        "source": source_name,
        "chunks_created": len(chunks),
        "total_vector_index_size": len(_GLOBAL_VECTOR_STORE.index)
    }, indent=2)

def get_global_vector_store() -> VectorStore:
    return _GLOBAL_VECTOR_STORE
