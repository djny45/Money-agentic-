from dataclasses import dataclass

@dataclass
class ContentVariant:
    id: str
    channel: str
    text: str

class ContentAgent:
    """Generates transparent promotional copy from supplied offer facts."""
    def variants(self, offer_title: str, destination: str, channel: str) -> list[ContentVariant]:
        return [
            ContentVariant(channel + "-a", channel,
                           offer_title + ". Check the current details here: " + destination),
            ContentVariant(channel + "-b", channel,
                           "Looking for " + offer_title + "? Review the offer details before deciding: " + destination),
        ]
