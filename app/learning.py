from dataclasses import dataclass

@dataclass
class LearningDecision:
    action: str
    reason: str
    confidence: float

class LearningEngine:
    """Evidence-based learning layer; it changes strategies, not executable code."""

    def evaluate(self, *, clicks: int, conversions: int, revenue: float,
                 sample_floor: int = 30) -> LearningDecision:
        if clicks < sample_floor:
            return LearningDecision(
                "collect_more_data",
                f"Only {clicks} clicks; minimum sample is {sample_floor}.",
                0.2,
            )
        cr = conversions / clicks if clicks else 0.0
        if conversions == 0:
            return LearningDecision("pause_experiment",
                                    "No measured conversions after minimum sample.",
                                    0.85)
        return LearningDecision("retain_and_test",
                                f"Measured conversion rate={cr:.4f}; run a controlled variant.",
                                min(0.95, 0.5 + conversions / 100))
