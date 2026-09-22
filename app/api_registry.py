from dataclasses import dataclass
import os

@dataclass(frozen=True)
class APIConfig:
    """Central registry for optional integrations.

    Secrets are read from environment variables only and are never stored in
    source code, SQLite, logs, or strategy memory.
    """
    cpagrip_api_key: str = os.getenv("CPAGRIP_API_KEY", "")
    cpagrip_api_url: str = os.getenv("CPAGRIP_API_URL", "")
    postiz_api_key: str = os.getenv("POSTIZ_API_KEY", "")
    postiz_api_url: str = os.getenv("POSTIZ_API_URL", "")
    bluesky_handle: str = os.getenv("BLUESKY_HANDLE", "")
    bluesky_app_password: str = os.getenv("BLUESKY_APP_PASSWORD", "")
    mastodon_access_token: str = os.getenv("MASTODON_ACCESS_TOKEN", "")
    mastodon_base_url: str = os.getenv("MASTODON_BASE_URL", "")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "phi3")

    def configured(self) -> dict[str, bool]:
        return {
            "cpagrip": bool(self.cpagrip_api_key and self.cpagrip_api_url),
            "postiz": bool(self.postiz_api_key and self.postiz_api_url),
            "bluesky": bool(self.bluesky_handle and self.bluesky_app_password),
            "mastodon": bool(self.mastodon_access_token and self.mastodon_base_url),
            "ollama": bool(self.ollama_url and self.ollama_model),
        }
