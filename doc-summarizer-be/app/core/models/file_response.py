from app.core.models.enum import FileType
from app.core.models.file_model import FileModel
from app.core.models.generic_response import AppResponse
from typing import List
from pydantic import BaseModel


class ExtractedFile(BaseModel):
    id: str
    file_name: str
    file_type: FileType
    file_size: int | None = None


class ExtractedFileResponse(ExtractedFile):
    created: str


class FileExtractionResponse(BaseModel):
    session_id: str
    files: List[ExtractedFile]


class FileUploadResponse(AppResponse):
    data: FileExtractionResponse


class GetFileResponse(ExtractedFileResponse):
    session_id: str


class GetFilesResponse(AppResponse):
    data: List[GetFileResponse]
