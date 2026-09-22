from .api_registry import APIConfig

def integration_status() -> dict[str, bool]:
    return APIConfig().configured()
