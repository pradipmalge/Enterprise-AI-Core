import json
import re
from typing import Dict, Any, List

class Document:
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"<Document source={self.metadata.get('source', 'unknown')} len={len(self.content)}>"

class DocumentLoader:
    """Enterprise Document Loader supporting TXT, Markdown, JSON, and structured text."""
    
    @staticmethod
    def load_from_text(text: str, source_name: str = "document.txt") -> Document:
        return Document(content=text, metadata={"source": source_name, "char_count": len(text)})

    @staticmethod
    def load_from_json(json_str: str, source_name: str = "data.json") -> List[Document]:
        try:
            data = json.loads(json_str)
            docs = []
            if isinstance(data, list):
                for idx, item in enumerate(data):
                    content = json.dumps(item, indent=2)
                    docs.append(Document(content=content, metadata={"source": f"{source_name}[{idx}]", "type": "json"}))
            elif isinstance(data, dict):
                for key, val in data.items():
                    content = f"Section {key}:\n{json.dumps(val, indent=2)}"
                    docs.append(Document(content=content, metadata={"source": f"{source_name}::{key}", "type": "json_section"}))
            return docs
        except Exception as e:
            return [Document(content=json_str, metadata={"source": source_name, "error": str(e)})]
