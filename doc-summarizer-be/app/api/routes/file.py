import logging
from fastapi import APIRouter, UploadFile, HTTPException, status, File, Query, Depends
from typing import List, Optional
from app import crud
from app.core.models.file import FileUploadResponse, GetFilesResponse
from app.core.models.session import Session
from app.core.utils.file import validate_file, index_files
from motor.core import AgnosticDatabase
from app.api import deps
from bson import ObjectId


router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
async def file_upload(
    db: AgnosticDatabase = Depends(deps.get_db),
    files: List[UploadFile] = File(...),
    session_id: Optional[str] = Query(None)
) -> FileUploadResponse:
    session = None
    if (session_id):
        session = await crud.session.get(db, id=ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid session ID provided.",
            )
    else:
        logging.info("Creating a new session")
        session = await crud.session.create(db=db)

    validate_file(files)
    session_id = str(session.id)
    extracted_files = await index_files(session_id, files)
    await crud.file.create_multi(
        db=db, obj_in=extracted_files, session_obj=session
    )
    return FileUploadResponse(data={"session_id": session_id, "files": extracted_files})


@router.get("/list")
async def list_files(
    db: AgnosticDatabase = Depends(deps.get_db),
    session_id: str = Query(...)
) -> GetFilesResponse:
    session = await crud.session.get(db, id=ObjectId(session_id))
    if (not session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    files = await crud.file.get_multi(db=db, session=session)
    return GetFilesResponse(data=files)
