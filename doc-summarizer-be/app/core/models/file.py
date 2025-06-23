from app.core.models.generic_response import AppResponse
from typing import List
from enum import StrEnum
from pydantic import BaseModel
from datetime import datetime
from odmantic import Field, Reference
from app.db.base_class import Base
from app.core.models.session import Session


class FileType(StrEnum):
    TEXT_TYPE = "text/plain"
    PDF_TYPE = "application/pdf"
    DOC_TYPE = "application/msword"
    DOCX_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class ExtractedFile(BaseModel):
    id: str
    file_name: str
    file_type: FileType


class FileExtractionResponse(BaseModel):
    session_id: str
    files: List[ExtractedFile]


class FileUploadResponse(AppResponse):
    data: FileExtractionResponse


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class FileModel(Base):
    created: datetime = Field(default_factory=datetime_now_sec)
    file_name: str = Field()
    file_type: FileType = Field()
    session_id: Session = Reference()


class GetFilesResponse(AppResponse):
    # data: List[FileModel]
    data: list
