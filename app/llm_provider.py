import os
from .ollama import OllamaClient
from .localai import LocalAIClient


def get_local_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    if provider == "localai":
        return LocalAIClient(
            os.getenv("LOCALAI_URL", "http://localai:8080"),
            os.getenv("LOCALAI_MODEL", "local-model"),
        )
    return OllamaClient(
        os.getenv("OLLAMA_URL", "http://ollama:11434"),
        os.getenv("OLLAMA_MODEL", "phi3"),
    )
