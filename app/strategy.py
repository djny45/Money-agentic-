from dataclasses import asdict
import json
from .models import Strategy

class StrategyManager:
    def propose(self, offer_title: str, channel: str) -> Strategy:
        return Strategy(
            name=f"{channel}:{offer_title[:40]}",
            hypothesis="A useful, transparent message tailored to the audience may improve qualified conversions.",
            actions=[
                "Create two compliant content variants.",
                "Use trackable campaign attribution.",
                "Publish only through an authorized channel.",
                "Measure clicks and conversions.",
                "Keep a variant only after sufficient sample."
            ],
            evidence={"channel": channel, "offer": offer_title},
        )

    def serialize(self, strategy: Strategy) -> str:
        return json.dumps(asdict(strategy), indent=2)
