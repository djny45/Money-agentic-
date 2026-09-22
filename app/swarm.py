from .learning import LearningEngine
from .strategy import StrategyManager

class MoneySwarm:
    """Coordinates specialized agents without unrestricted self-modification."""

    def __init__(self):
        self.learning = LearningEngine()
        self.strategy = StrategyManager()

    def plan(self, offer_title: str, channel: str) -> dict:
        strategy = self.strategy.propose(offer_title, channel)
        return {
            "role": "orchestrator",
            "strategy": strategy,
            "pipeline": [
                "research",
                "score_offer",
                "generate_content",
                "compliance_check",
                "queue_authorized_publisher",
                "measure",
                "learn",
            ],
        }
