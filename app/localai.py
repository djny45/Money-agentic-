import httpx


class LocalAIClient:
    """OpenAI-compatible local inference client for a self-hosted LocalAI server."""

    def __init__(self, base_url: str = "http://127.0.0.1:8080", model: str = "gpt-4o-mini",
                 timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.base_url + "/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
