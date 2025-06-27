from __future__ import annotations
from datetime import datetime
from odmantic import Field, ObjectId
from pydantic import BaseModel
from app.db.base_class import Base
from app.core.models.util import datetime_now_sec


class Session(Base):
    created: datetime = Field(default_factory=datetime_now_sec)
    session_name: str = Field(default="")
    files: list[ObjectId] = Field(default_factory=list)


class UpdateSession(BaseModel):
    session_name: str = Field(default="")
