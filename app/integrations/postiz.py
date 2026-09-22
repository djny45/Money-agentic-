import httpx
from .base import IntegrationHealth

class PostizClient:
    name = "postiz"

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    async def health(self) -> IntegrationHealth:
        if not self.api_url or not self.api_key:
            return IntegrationHealth(self.name, False, False, "not configured")
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.api_url}/public/v1/integrations", headers=self._headers())
            return IntegrationHealth(self.name, True, response.is_success, f"HTTP {response.status_code}")
        except Exception as exc:
            return IntegrationHealth(self.name, True, False, type(exc).__name__)

    async def list_integrations(self, group: str | None = None) -> dict:
        params = {"group": group} if group else None
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{self.api_url}/public/v1/integrations",
                headers=self._headers(),
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def create_post(
        self,
        content: str,
        integration_ids: list[str],
        scheduled_at: str,
        *,
        draft: bool = True,
        short_link: bool = True,
    ) -> dict:
        if not content.strip():
            raise ValueError("content must not be empty")
        if not integration_ids:
            raise ValueError("at least one authorized integration is required")
        payload = {
            "type": "draft" if draft else "schedule",
            "date": scheduled_at,
            "posts": [{
                "integration": {"id": integration_id},
                "value": [{"content": content, "image": []}],
            } for integration_id in integration_ids],
            "shortLink": short_link,
            "creationMethod": "API",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{self.api_url}/public/v1/posts",
                headers=self._headers(),
                json=payload,
            )
            response.raise_for_status()
            return response.json()
