from typing import List
from pydantic import BaseModel
from app.core.models.generic_response import AppResponse
from app.core.models.enum import FileType
from app.core.models.session_model import Session


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
