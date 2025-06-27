from typing import List
from pydantic import BaseModel
from app.core.models.file_response import ExtractedFileResponse
from app.core.models.generic_response import AppResponse
from app.core.models.session_model import Session


class CreateSessionResponse(AppResponse):
    data: Session


class GetSessionsResponse(AppResponse):
    data: List[Session]


class GetSessionByID(BaseModel):
    id: str
    session_name: str
    created: str
    files: List[ExtractedFileResponse]


class GetSessionByIDResponse(AppResponse):
    data: GetSessionByID
