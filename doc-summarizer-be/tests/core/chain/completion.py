from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from core.chain.prompts import get_chat_prompt_template
from core.config import Settings
from core.models.completion_response import CompletionResponse


class Completion:
    def __init__(self):
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
        chat_prompt_template = get_chat_prompt_template()
        self.chain = chat_prompt_template | self.model

    async def invoke(self, params: dict) -> CompletionResponse:
        print(f"Invoking completion with query: {params.get('query')}")
        query = params.get("query")
        context = params.get("context")
        chat_history = params.get("chat_history") or []
        response = await self.chain.ainvoke({"user_input": query, "context": context, "messages": chat_history})
        usage_metadata = (response.to_json().get(
            "kwargs", {}).get("usage_metadata", {}))
        content = response.text()
        return CompletionResponse(content=content, usage_metadata=usage_metadata)

    async def invoke_with_retry(self, *, query: str, context: str, chat_history: list[dict] | None = []) -> CompletionResponse:
        runnable = RunnableLambda(self.invoke)
        return await runnable.with_retry(
            stop_after_attempt=3,
            wait_exponential_jitter=True
        ).ainvoke({"query": query, "context": context, "chat_history": chat_history})


chat_completion = Completion()
