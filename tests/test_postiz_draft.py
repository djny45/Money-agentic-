import pytest
from unittest.mock import AsyncMock, patch

from app.api_service import create_postiz_draft


@pytest.mark.asyncio
async def test_postiz_draft_uses_draft_mode():
    with patch("app.api_service.APIConfig") as cfg_cls, patch("app.api_service.PostizClient") as client_cls:
        cfg = cfg_cls.return_value
        cfg.postiz_api_url = "https://postiz.example"
        cfg.postiz_api_key = "secret"
        client = client_cls.return_value
        client.create_post = AsyncMock(return_value={"status": "draft"})
        result = await create_postiz_draft("hello", ["integration-1"], "2030-01-01T10:00:00Z")
        assert result["status"] == "draft"
        client.create_post.assert_awaited_once_with(
            "hello", ["integration-1"], "2030-01-01T10:00:00Z",
            draft=True, short_link=True
        )
