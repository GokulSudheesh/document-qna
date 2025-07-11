import logging
from fastapi import APIRouter, UploadFile, File, Query, Depends
from typing import List, Optional
from app import crud
from app.core.models.file_response import GetFilesResponse, FileUploadResponse
from app.core.models.generic_response import DeleteByIDResponse
from app.core.models.session_model import Session
from app.core.utils.file import validate_file, index_files
from motor.core import AgnosticDatabase
from app.api import deps


router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload")
async def file_upload(
    db: AgnosticDatabase = Depends(deps.get_db),
    files: List[UploadFile] = File(...),
    session_id: Optional[str] = Query(None)
) -> FileUploadResponse:
    session = None
    if (session_id):
        session = await deps.get_session(session_id, db)
        await crud.session.update_session_updated_at(db, db_obj=session)
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
    session: Session = Depends(deps.get_session)
) -> GetFilesResponse:
    files = await crud.file.get_multi(db=db, session=session)
    return GetFilesResponse(data=files)


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    db: AgnosticDatabase = Depends(deps.get_db)
) -> DeleteByIDResponse:
    logging.info(f"Deleting file with ID: {file_id}")
    file = await crud.file.remove(db=db, id=file_id)
    session_id = file.session_id.id
    session = await deps.get_session(session_id, db)
    await crud.session.update_session_updated_at(db, db_obj=session)
    return DeleteByIDResponse(data={"id": file_id, "message": "File deleted successfully."})
