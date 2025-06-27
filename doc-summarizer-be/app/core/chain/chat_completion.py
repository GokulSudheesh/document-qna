from langchain_core.runnables import RunnableLambda
from app.core.chain.base_completion import CompletionBase
from app.core.chain.prompts import get_chat_prompt_template
from app.core.models.chat_model import TransformedChatModel
from app.core.models.completion_model import CompletionResponse
from typing import Any, AsyncGenerator, AsyncIterator, List
import logging


class ChatCompletion(CompletionBase):
    def __init__(self):
        super().__init__()
        chat_prompt_template = get_chat_prompt_template()
        self.chain = chat_prompt_template | self.model

    async def invoke(self, params: dict) -> CompletionResponse:
        logging.info(f"Invoking completion with query: {params.get('query')}")
        query = params.get("query")
        context = params.get("context")
        chat_history = params.get("chat_history") or []
        response = await self.chain.ainvoke({"user_input": query, "context": context, "messages": chat_history})
        usage_metadata = (response.to_json().get(
            "kwargs", {}).get("usage_metadata", {}))
        content = response.text()
        return CompletionResponse(content=content, usage_metadata=usage_metadata)

    async def astream(self, params: dict) -> AsyncGenerator[str, Any]:
        query = params.get("query")
        context = params.get("context")
        chat_history = params.get("chat_history") or []
        logging.info(f"Streaming completion with query: {query}")
        input = {"user_input": query,
                 "context": context, "messages": chat_history}
        async for chunk in self.chain.astream(input):
            if (not chunk or not chunk.text()):
                continue
            # logging.info(f"Chunk: {chunk.text()}")
            yield chunk.content

    async def invoke_with_retry(self, *, query: str, context: str, chat_history: List[TransformedChatModel] | None = []) -> CompletionResponse:
        runnable = RunnableLambda(self.invoke)
        return await runnable.with_retry(
            stop_after_attempt=self.retry_count,
            wait_exponential_jitter=True
        ).ainvoke({"query": query, "context": context, "chat_history": chat_history})

    def astream_with_retry(self, *, query: str, context: str, chat_history: List[TransformedChatModel] | None = []) -> AsyncIterator[str]:
        runnable = RunnableLambda(self.astream)
        return runnable.with_retry(
            stop_after_attempt=self.retry_count,
            wait_exponential_jitter=True
        ).astream({"query": query, "context": context, "chat_history": chat_history})


chat_completion = ChatCompletion()
