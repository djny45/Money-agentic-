from .learning import LearningEngine
from .strategy import StrategyManager
from .offer_intelligence import OfferIntelligence
from .content import ContentAgent
from .compliance import ComplianceAgent
from .queue import PublishQueue
from .banner import BannerAgent, BannerBrief
from .ad_publisher import AdPublisher

class MoneySwarm:
    """Coordinates specialized agents with measurable, policy-gated workflows."""

    def __init__(self):
        self.learning = LearningEngine()
        self.strategy = StrategyManager()
        self.offers = OfferIntelligence()
        self.content = ContentAgent()
        self.compliance = ComplianceAgent()
        self.queue = PublishQueue()
        self.banner = BannerAgent()
        self.ad_publisher = AdPublisher()

    def plan(self, offer_title: str, channel: str) -> dict:
        strategy = self.strategy.propose(offer_title, channel)
        variants = self.content.variants(offer_title, "[TRACKED_URL]", channel)
        banner = self.banner.build_svg(BannerBrief(
            title=offer_title,
            subtitle="Review the current offer details before deciding.",
            call_to_action="Learn more",
        ))
        return {
            "role": "orchestrator",
            "strategy": strategy,
            "content_variants": variants,
            "banner_svg": banner,
            "pipeline": [
                "research",
                "score_offer_from_observed_data",
                "generate_content",
                "compliance_check",
                "queue_authorized_publisher",
                "measure_real_results",
                "learn_from_evidence",
                "version_strategy",
                "rollback_on_regression",
            ],
        }
