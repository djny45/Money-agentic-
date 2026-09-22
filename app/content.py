from dataclasses import dataclass
from .llm_api import LLMAPIClient


@dataclass
class ContentVariant:
    id: str
    channel: str
    text: str


class ContentAgent:
    """Generate transparent promotional variants.

    The hosted LLM is optional and is used only to draft copy. Publishing remains
    a separate, approval-gated operation.
    """

    def __init__(self, llm: LLMAPIClient | None = None):
        self.llm = llm

    def variants(self, offer_title: str, destination: str, channel: str) -> list[ContentVariant]:
        return [
            ContentVariant(
                channel + "-a",
                channel,
                offer_title + ". Check the current details here: " + destination,
            ),
            ContentVariant(
                channel + "-b",
                channel,
                "Looking for " + offer_title + "? Review the offer details before deciding: " + destination,
            ),
        ]

    async def llm_variant(self, offer_title: str, destination: str, channel: str) -> ContentVariant:
        if self.llm is None:
            raise RuntimeError("LLM API client is not configured")
        prompt = (
            "Draft one concise, factual promotional variant. "
            "Do not invent claims, scarcity, discounts, testimonials, or guarantees. "
            "Clearly identify the destination as an offer link. "
            f"Offer title: {offer_title}\nChannel: {channel}\nDestination: {destination}"
        )
        text = (await self.llm.generate(prompt)).strip()
        if not text:
            raise ValueError("LLM returned empty content")
        return ContentVariant(channel + "-llm", channel, text)
