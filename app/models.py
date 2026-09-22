from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class Offer:
    id: str
    title: str
    url: str
    payout: float
    country: str = "IN"
    category: str = ""
    conversion_rate: float | None = None
    epc: float | None = None
    active: bool = True

@dataclass
class Experiment:
    id: str
    offer_id: str
    channel: str
    variant: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    started_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions else 0.0

    @property
    def conversion_rate(self) -> float:
        return self.conversions / self.clicks if self.clicks else 0.0

@dataclass
class Strategy:
    name: str
    hypothesis: str
    actions: list[str]
    evidence: dict[str, Any] = field(default_factory=dict)
    version: int = 1
