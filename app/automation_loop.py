import asyncio
import os
from datetime import datetime, timezone

from .autopilot import run_autopilot
from .optimizer import optimize_experiments


async def run_cycle() -> dict:
    """Execute one bounded autonomous optimization cycle."""
    channel = os.getenv("AUTOPILOT_CHANNEL", "postiz")
    limit = int(os.getenv("AUTOPILOT_LIMIT", "5"))
    sample_floor = int(os.getenv("MIN_EXPERIMENT_SAMPLE", "30"))

    optimization = await optimize_experiments(sample_floor=sample_floor)
    autopilot = await run_autopilot(channel=channel, limit=limit)
    return {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "optimization": optimization,
        "autopilot": autopilot,
    }


def main() -> None:
    asyncio.run(run_cycle())


if __name__ == "__main__":
    main()
