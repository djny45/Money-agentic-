from app.analytics import CampaignMetrics
from app.compliance import ComplianceAgent
from app.models import Offer
from app.offer_intelligence import OfferIntelligence
from app.tracking import add_utm

def test_offer_score_uses_observed_metrics():
    score = OfferIntelligence().score(
        Offer("1", "Offer", "https://example.test", 0.17, conversion_rate=0.02, epc=0.04)
    )
    assert score.score > 0
    assert any("payout" in x for x in score.reasons)

def test_utm_preserves_existing_query():
    url = add_utm("https://example.test/path?a=1", source="social", medium="organic", campaign="x")
    assert "a=1" in url and "utm_source=social" in url

def test_compliance_blocks_unauthorized():
    result = ComplianceAgent().check(authorized=False)
    assert not result.allowed

def test_metrics():
    m = CampaignMetrics(impressions=100, clicks=10, conversions=2, revenue=0.34)
    assert m.ctr == 0.1
    assert m.conversion_rate == 0.2
