from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.rate_limiters import InMemoryRateLimiter
from app.core.config import Settings


class CompletionBase:
    def __init__(self):
        self.retry_count = 3
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
