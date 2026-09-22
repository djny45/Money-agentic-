import csv
import io
import json
import xml.etree.ElementTree as ET
import httpx
from .base import IntegrationHealth

class CPAGripClient:
    name = "cpagrip"

    def __init__(self, api_url: str, api_key: str = ""):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    async def health(self) -> IntegrationHealth:
        if not self.api_url:
            return IntegrationHealth(self.name, False, False, "offer feed URL not configured")
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                response = await client.get(self.api_url, headers=self._headers())
            return IntegrationHealth(self.name, True, response.is_success, f"HTTP {response.status_code}")
        except Exception as exc:
            return IntegrationHealth(self.name, True, False, type(exc).__name__)

    @staticmethod
    def _normalise(item: dict) -> dict:
        lower = {str(k).lower().strip(): v for k, v in item.items()}
        def first(*keys, default=""):
            for key in keys:
                value = lower.get(key)
                if value not in (None, ""):
                    return value
            return default
        payout_raw = first("payout", "amount", "commission", default=0)
        try:
            payout = float(str(payout_raw).replace("$", "").strip())
        except (TypeError, ValueError):
            payout = 0.0
        return {
            "id": str(first("id", "offer_id", "offerid", default="")),
            "title": str(first("title", "name", "offer_name", default="")),
            "url": str(first("url", "offer_url", "link", "tracking_url", default="")),
            "payout": payout,
            "country": str(first("country", "geo", "country_code", default="")),
            "category": str(first("category", "vertical", "type", default="")),
        }

    @classmethod
    def parse_feed(cls, body: str, content_type: str = "") -> list[dict]:
        text = body.strip()
        if not text:
            return []
        if "json" in content_type.lower() or text[:1] in "[{":
            data = json.loads(text)
            if isinstance(data, dict):
                data = data.get("offers", data.get("data", []))
            return [cls._normalise(x) for x in data if isinstance(x, dict)]
        if "xml" in content_type.lower() or text.startswith("<"):
            root = ET.fromstring(text)
            rows = []
            for node in root.iter():
                if node is root:
                    continue
                fields = {child.tag.split("}")[-1]: (child.text or "") for child in list(node)}
                if fields and any(k.lower() in fields for k in ("id", "offer_id", "title", "name", "url")):
                    rows.append(cls._normalise(fields))
            return rows
        reader = csv.DictReader(io.StringIO(text))
        return [cls._normalise(row) for row in reader]

    async def fetch_offers(self) -> list[dict]:
        if not self.api_url:
            return []
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(self.api_url, headers=self._headers())
            response.raise_for_status()
            return self.parse_feed(response.text, response.headers.get("content-type", ""))
