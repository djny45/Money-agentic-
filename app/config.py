import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    mode: str = os.getenv("MODE", "DRY_RUN")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/money_agentic.db")
    default_country: str = os.getenv("DEFAULT_COUNTRY", "IN")
    max_daily_posts: int = int(os.getenv("MAX_DAILY_POSTS", "20"))
    min_experiment_sample: int = int(os.getenv("MIN_EXPERIMENT_SAMPLE", "30"))
    auto_publish: bool = os.getenv("AUTO_PUBLISH", "false").lower() == "true"
    control_token: str = os.getenv("CONTROL_PANEL_TOKEN", "")

settings = Settings()
