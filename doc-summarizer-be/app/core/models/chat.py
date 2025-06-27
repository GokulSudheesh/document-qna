from pydantic import BaseModel
from app.core.models.completion_model import CompletionResponseWithReferences
from app.core.models.generic_response import AppResponse


class ChatRequestBody(BaseModel):
    query: str


class ChatResponse(AppResponse):
    data: CompletionResponseWithReferences
