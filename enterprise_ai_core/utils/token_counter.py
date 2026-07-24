import tiktoken
from typing import Optional

class TokenCounter:
    @staticmethod
    def count_tokens(text: str, model: str = "gpt-4o") -> int:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            # Approx word count * 1.3
            return int(len(text.split()) * 1.3) + 1
