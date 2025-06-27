from datetime import datetime
from typing import Optional
from odmantic import Field, ObjectId, Reference
from pydantic import BaseModel
from app.core.models.util import datetime_now_sec
from app.db.base_class import Base
from app.core.models.enum import MessageRole
from app.core.models.session_model import Session


class ChatModel(Base):
    session_id: Session = Reference()
    created: datetime = Field(default_factory=datetime_now_sec)
    role: MessageRole = Field()
    message: str = Field(default="")
    references: Optional[list[ObjectId]] = Field(default=None)


class TransformedChatModel(BaseModel):
    role: MessageRole = Field()
    content: str = Field()
