from dataclasses import dataclass
from .analytics import CampaignMetrics

@dataclass
class AttributionEvent:
    campaign: str
    source: str
    content: str
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0

class Attribution:
    def summarize(self, events: list[AttributionEvent]) -> dict:
        metrics = CampaignMetrics(
            clicks=sum(e.clicks for e in events),
            conversions=sum(e.conversions for e in events),
            revenue=sum(e.revenue for e in events))
        return {
            "clicks": metrics.clicks,
            "conversions": metrics.conversions,
            "revenue": round(metrics.revenue, 4),
            "conversion_rate": round(metrics.conversion_rate, 6),
            "epc": round(metrics.epc, 6),
        }
