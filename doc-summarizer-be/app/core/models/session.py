from __future__ import annotations
from datetime import datetime
from typing import List
from odmantic import Field, ObjectId
from app.db.base_class import Base
from app.core.models.generic_response import AppResponse


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class Session(Base):
    created: datetime = Field(default_factory=datetime_now_sec)
    session_name: str = Field(default="")
    files: list[ObjectId] = Field(default_factory=list)


class CreateSessionResponse(AppResponse):
    data: Session


class GetSessionsResponse(AppResponse):
    data: List[Session]
