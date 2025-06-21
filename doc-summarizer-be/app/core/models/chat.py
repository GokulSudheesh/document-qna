from pydantic import BaseModel
from app.core.models.completion_response import CompletionResponseWithReferences
from app.core.models.generic_response import AppResponse


class ChatRequestBody(BaseModel):
    session_id: str
    query: str


class ChatResponse(AppResponse):
    data: CompletionResponseWithReferences
