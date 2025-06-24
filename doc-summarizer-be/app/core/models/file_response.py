from app.core.models.enum import FileType
from app.core.models.generic_response import AppResponse
from typing import List
from pydantic import BaseModel


class ExtractedFile(BaseModel):
    id: str
    file_name: str
    file_type: FileType


class FileExtractionResponse(BaseModel):
    session_id: str
    files: List[ExtractedFile]


class FileUploadResponse(AppResponse):
    data: FileExtractionResponse


class GetFileResponse(BaseModel):
    id: str
    session_id: str
    file_name: str
    file_type: FileType


class GetFilesResponse(AppResponse):
    data: List[GetFileResponse]
