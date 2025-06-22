from app.core.models.generic_response import AppResponse
from typing import List
from enum import StrEnum
from pydantic import BaseModel


class FileType(StrEnum):
    TEXT_TYPE = "text/plain"
    PDF_TYPE = "application/pdf"
    DOC_TYPE = "application/msword"
    DOCX_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class ExtractedFile(BaseModel):
    file_id: str
    file_name: str
    file_type: FileType


class FileExtractionResponse(BaseModel):
    session_id: str
    extracted_files: List[ExtractedFile]


class FileUploadResponse(AppResponse):
    data: FileExtractionResponse
