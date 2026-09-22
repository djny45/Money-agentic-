from dataclasses import dataclass

@dataclass
class ComplianceResult:
    allowed: bool
    reasons: list[str]

class ComplianceAgent:
    """Conservative gate for publishing and experiments."""

    def check(self, *, authorized: bool, fake_traffic: bool = False,
              spam: bool = False, prohibited_incentive: bool = False) -> ComplianceResult:
        reasons = []
        if not authorized:
            reasons.append("Publisher account is not authorized.")
        if fake_traffic:
            reasons.append("Artificial traffic is prohibited.")
        if spam:
            reasons.append("Spam behavior is prohibited.")
        if prohibited_incentive:
            reasons.append("Offer/platform incentive rules may be violated.")
        return ComplianceResult(not reasons, reasons)
