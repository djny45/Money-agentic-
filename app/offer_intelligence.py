from dataclasses import dataclass
from .models import Offer

@dataclass(frozen=True)
class OfferScore:
    offer_id: str
    score: float
    reasons: list[str]

class OfferIntelligence:
    """Ranks offers from observed, supplied metrics; never invents conversion data."""
    def score(self, offer: Offer) -> OfferScore:
        score = 0.0
        reasons = []
        if offer.payout > 0:
            score += min(40.0, offer.payout * 20)
            reasons.append("payout=$%.2f" % offer.payout)
        if offer.conversion_rate is not None:
            score += min(35.0, offer.conversion_rate * 100)
            reasons.append("CR=%.2f%%" % (offer.conversion_rate * 100))
        if offer.epc is not None:
            score += min(25.0, offer.epc * 100)
            reasons.append("EPC=$%.2f" % offer.epc)
        if not offer.active:
            score = 0.0
            reasons.append("inactive")
        return OfferScore(offer.id, round(score, 3), reasons)
