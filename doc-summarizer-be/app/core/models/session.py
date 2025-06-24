from __future__ import annotations
from datetime import datetime
from typing import List
from odmantic import Field, ObjectId
from pydantic import BaseModel
from app.db.base_class import Base
from app.core.models.generic_response import AppResponse
from app.core.models.enum import FileType


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


class GetFileResponse(BaseModel):
    id: str
    file_name: str
    file_type: FileType


class GetSessionByID(BaseModel):
    id: str
    session_name: str
    created: str
    files: List[GetFileResponse]


class GetSessionByIDResponse(AppResponse):
    data: GetSessionByID
