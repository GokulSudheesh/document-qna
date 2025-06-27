import re
from langchain_core.runnables import RunnableLambda
from app.core.chain.base_completion import CompletionBase
from app.core.chain.prompts import session_name_prompt_template
from app.core.models.chat_model import TransformedChatModel
from typing import List


class SessionNameCompletion(CompletionBase):
    def __init__(self):
        super().__init__()
        self.chain = session_name_prompt_template | self.model

    async def invoke(self, params: dict) -> str:
        chat_history = params.get("chat_history") or []
        response = await self.chain.ainvoke({"context": chat_history})
        content = response.text()
        content = re.sub(r'[\"]', "", content)
        return content

    async def invoke_with_retry(self, *, chat_history: List[TransformedChatModel] | None = []) -> str:
        runnable = RunnableLambda(self.invoke)
        return await runnable.with_retry(
            stop_after_attempt=self.retry_count,
            wait_exponential_jitter=True
        ).ainvoke({"chat_history": chat_history})


session_name_completion = SessionNameCompletion()
