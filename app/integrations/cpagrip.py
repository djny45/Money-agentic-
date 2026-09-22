import httpx
from .base import IntegrationHealth

class CPAGripClient:
    name = "cpagrip"

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key

    async def health(self) -> IntegrationHealth:
        if not self.api_url or not self.api_key:
            return IntegrationHealth(self.name, False, False, "not configured")
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
            return IntegrationHealth(self.name, True, response.is_success, f"HTTP {response.status_code}")
        except Exception as exc:
            return IntegrationHealth(self.name, True, False, type(exc).__name__)
