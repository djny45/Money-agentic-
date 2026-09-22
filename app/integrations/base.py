from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class IntegrationHealth:
    provider: str
    configured: bool
    reachable: bool
    detail: str

class Integration(Protocol):
    name: str
    async def health(self) -> IntegrationHealth: ...
