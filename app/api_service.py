from .api_registry import APIConfig
from .integrations.cpagrip import CPAGripClient
from .integrations.postiz import PostizClient


def integration_status() -> dict[str, bool]:
    return APIConfig().configured()
