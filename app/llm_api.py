import httpx


class LLMAPIClient:
    """Generic hosted LLM API client; credentials stay in deployment environment."""

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def health(self) -> bool:
        if not self.base_url or not self.api_key or not self.model:
            return False
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(self.base_url)
                return response.is_success
        except Exception:
            return False

    async def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
