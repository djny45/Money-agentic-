from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class QueueItem:
    channel: str
    text: str
    url: str
    created_at: str
    approved: bool = False

class PublishQueue:
    def __init__(self):
        self.items: list[QueueItem] = []

    def add(self, channel: str, text: str, url: str) -> QueueItem:
        item = QueueItem(channel, text, url, datetime.now(timezone.utc).isoformat())
        self.items.append(item)
        return item

    def approve(self, index: int) -> QueueItem:
        item = self.items[index]
        item.approved = True
        return item
