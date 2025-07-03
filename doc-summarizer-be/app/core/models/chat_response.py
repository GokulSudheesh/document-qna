from typing import List, Optional
from pydantic import BaseModel
from app.core.models.enum import MessageRole
from app.core.models.generic_response import AppResponse


class ChatFileReference(BaseModel):
    id: str
    file_name: str


class ChatHistoryItem(BaseModel):
    id: str
    created: str
    session_id: str
    role: MessageRole
    message: str
    references: Optional[List[ChatFileReference]]


class ChatHistoryResponse(AppResponse):
    data: List[ChatHistoryItem]
