from fastapi import APIRouter, UploadFile, File, Query
from typing import List, Optional
from app.core.utils.file import validate_file

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
async def file_upload(
    files: List[UploadFile] = File(...),
    session_id: Optional[str] = Query(None)
):
    validate_file(files)
    file_names = []
    for upload_file in files:
        file_names.append(upload_file.filename)
    return {"filenames": file_names, "session_id": session_id}
