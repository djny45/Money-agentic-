import pytest
from unittest.mock import AsyncMock

from app.content import ContentAgent
from app.llm_api import LLMAPIClient


@pytest.mark.asyncio
async def test_llm_variant_is_draft_only():
    client = LLMAPIClient("https://example.test", "key", "model")
    client.generate = AsyncMock(return_value="Transparent draft")
    variant = await ContentAgent(client).llm_variant("Example", "https://example.test/offer", "social")
    assert variant.id == "social-llm"
    assert variant.text == "Transparent draft"
