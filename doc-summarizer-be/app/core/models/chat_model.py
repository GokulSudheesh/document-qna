from datetime import datetime
from odmantic import Field, Reference
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


class TransformedChatModel(BaseModel):
    role: MessageRole = Field()
    content: str = Field()
