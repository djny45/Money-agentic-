from .api_registry import APIConfig
from .integrations.cpagrip import CPAGripClient
from .integrations.postiz import PostizClient
from .integrations.openaffiliate import OpenAffiliateClient


def integration_status() -> dict[str, bool]:
    return APIConfig().configured()


async def fetch_cpagrip_offers() -> list[dict]:
    cfg = APIConfig()
    if not cfg.cpagrip_api_url:
        return []
    return await CPAGripClient(cfg.cpagrip_api_url, cfg.cpagrip_api_key).fetch_offers()


async def postiz_integrations() -> dict:
    cfg = APIConfig()
    if not cfg.postiz_api_url or not cfg.postiz_api_key:
        return {"configured": False, "integrations": []}
    client = PostizClient(cfg.postiz_api_url, cfg.postiz_api_key)
    return {"configured": True, "integrations": await client.list_integrations()}


async def search_openaffiliate(query: str = "", category: str | None = None, commission_type: str | None = None, verified: bool | None = None) -> list[dict]:
    return await OpenAffiliateClient().search(query, category, commission_type, verified)
