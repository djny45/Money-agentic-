from dataclasses import dataclass
from datetime import datetime

@dataclass
class KnowledgeItem:
    source: str
    topic: str
    content: str
    captured_at: str

class ResearchAgent:
    """Stores research facts; it does not blindly execute discovered code."""

    def normalize(self, source: str, topic: str, content: str) -> KnowledgeItem:
        return KnowledgeItem(source, topic, content.strip(), datetime.utcnow().isoformat())
