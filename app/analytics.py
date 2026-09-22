from dataclasses import dataclass

@dataclass
class CampaignMetrics:
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    spend: float = 0.0

    @property
    def ctr(self):
        return self.clicks / self.impressions if self.impressions else 0.0

    @property
    def conversion_rate(self):
        return self.conversions / self.clicks if self.clicks else 0.0

    @property
    def profit(self):
        return self.revenue - self.spend

    @property
    def epc(self):
        return self.revenue / self.clicks if self.clicks else 0.0
