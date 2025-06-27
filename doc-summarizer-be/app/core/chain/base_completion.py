from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_ollama import ChatOllama
from langchain_core.rate_limiters import InMemoryRateLimiter
from app.core.config import Settings
import logging

from app.core.models.enum import Platform


class CompletionBase:
    def __init__(self):
        logging.info(
            f"Using {Settings.PLATFORM_TO_USE.upper()} platform for completion")
        self.retry_count = 3
        match Settings.PLATFORM_TO_USE:
            case Platform.NVIDIA:
                rate_limiter = InMemoryRateLimiter(
                    # <-- Super slow! Sadly, we can only make a request once every 10 seconds!!
                    requests_per_second=0.1,
                    # Wake up every 100 ms to check whether allowed to make a request,
                    check_every_n_seconds=0.1,
                    max_bucket_size=10,  # Controls the maximum burst size.
                )
                self.model = ChatNVIDIA(
                    **Settings.NVIDIA_MODEL_CONFIG,
                    rate_limiter=rate_limiter
                )
            case Platform.OLLAMA:
                self.model = ChatOllama(
                    **Settings.OLLAMA_MODEL_CONFIG,
                )
