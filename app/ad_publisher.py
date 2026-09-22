from dataclasses import dataclass


@dataclass(frozen=True)
class AdUploadRequest:
    platform: str
    creative_path: str
    campaign_id: str
    approved: bool = False


class AdPublisher:
    """Approval-gated interface for uploading creatives through official ad APIs."""

    def upload(self, request: AdUploadRequest) -> dict:
        if not request.approved:
            return {"status": "queued", "reason": "approval_required"}
        return {
            "status": "not_configured",
            "platform": request.platform,
            "reason": "official_platform_adapter_required",
        }
