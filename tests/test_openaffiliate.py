import pytest
from unittest.mock import AsyncMock, patch

from app.integrations.openaffiliate import OpenAffiliateClient


@pytest.mark.asyncio
async def test_openaffiliate_search():
    response = AsyncMock()
    response.json.return_value = [{"slug": "example", "name": "Example"}]
    response.raise_for_status = lambda: None
    with patch("httpx.AsyncClient.get", return_value=response):
        result = await OpenAffiliateClient().search("email")
    assert result[0]["slug"] == "example"
