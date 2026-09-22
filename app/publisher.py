from dataclasses import dataclass

@dataclass
class PublishRequest:
    channel: str
    text: str
    url: str
    approved: bool = False

class Publisher:
    """Dry-run publisher interface. Real adapters must use authorized APIs."""

    def publish(self, request: PublishRequest) -> dict:
        if not request.approved:
            return {"status": "queued", "reason": "approval_required"}
        return {"status": "not_configured", "channel": request.channel}
