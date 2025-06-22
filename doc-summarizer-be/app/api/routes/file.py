from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Query
from typing import List, Optional
from app.core.models.file import FileUploadResponse
from app.core.utils.file import validate_file, index_files

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
async def file_upload(
    files: List[UploadFile] = File(...),
    session_id: Optional[str] = Query(None)
) -> FileUploadResponse:
    session_id = session_id or str(uuid4())
    validate_file(files)
    extracted_files = await index_files(session_id, files)
    return FileUploadResponse(data={"session_id": session_id, "extracted_files": extracted_files})
