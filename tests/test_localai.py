from unittest.mock import AsyncMock, patch
import pytest

from app.localai import LocalAIClient


@pytest.mark.asyncio
async def test_localai_generate():
    response = AsyncMock()
    response.json.return_value = {"choices": [{"message": {"content": "hello"}}]}
    response.raise_for_status = lambda: None
    with patch("httpx.AsyncClient.post", return_value=response):
        result = await LocalAIClient().generate("test")
    assert result == "hello"
