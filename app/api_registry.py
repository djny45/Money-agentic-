from dataclasses import dataclass
import os


@dataclass(frozen=True)
class APIConfig:
    """Central registry for optional external API sessions.

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
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_api_url: str = os.getenv("LLM_API_URL", "")
    llm_model: str = os.getenv("LLM_MODEL", "")

    def configured(self) -> dict[str, bool]:
        return {
            "cpagrip": bool(self.cpagrip_api_key and self.cpagrip_api_url),
            "postiz": bool(self.postiz_api_key and self.postiz_api_url),
            "bluesky": bool(self.bluesky_handle and self.bluesky_app_password),
            "mastodon": bool(self.mastodon_access_token and self.mastodon_base_url),
            "llm_api": bool(self.llm_api_key and self.llm_api_url and self.llm_model),
        }
