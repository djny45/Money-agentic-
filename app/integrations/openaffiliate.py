import httpx


class OpenAffiliateClient:
    """Read-only client for the public OpenAffiliate registry.

    Uses the project's public REST API and does not submit, purchase, or
    manipulate affiliate programs.
    """

    name = "openaffiliate"

    def __init__(self, base_url: str = "https://openaffiliate.dev/api"):
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str = "", category: str | None = None,
                     commission_type: str | None = None,
                     verified: bool | None = None) -> list[dict]:
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if category:
            params["category"] = category
        if commission_type:
            params["type"] = commission_type
        if verified is not None:
            params["verified"] = str(verified).lower()

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/programs", params=params)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else data.get("programs", [])

    async def get_program(self, slug: str) -> dict:
        if not slug.strip():
            raise ValueError("slug must not be empty")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/programs/{slug}")
            response.raise_for_status()
            return response.json()
