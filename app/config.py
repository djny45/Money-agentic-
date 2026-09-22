import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    mode: str = os.getenv("MODE", "DRY_RUN")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/money_agentic.db")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "phi3")
    default_country: str = os.getenv("DEFAULT_COUNTRY", "IN")
    max_daily_posts: int = int(os.getenv("MAX_DAILY_POSTS", "20"))
    min_experiment_sample: int = int(os.getenv("MIN_EXPERIMENT_SAMPLE", "30"))
    auto_publish: bool = os.getenv("AUTO_PUBLISH", "false").lower() == "true"

settings = Settings()
