from typing import List
from pydantic import BaseModel
from app.core.models.generic_response import AppResponse


class ChatHistoryItem(BaseModel):
    id: str
    created: str
    session_id: str
    role: str
    message: str


class ChatHistoryResponse(AppResponse):
    data: List[ChatHistoryItem]
