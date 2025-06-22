import logging
from typing import List
from fastapi import UploadFile, HTTPException, status
from app.core.config import Settings


def validate_file(files: List[UploadFile]) -> bool:
    for file in files:
        if file.size >= Settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"File size exceeds the limit of {Settings.MAX_FILE_SIZE_STR} for {file.filename}")
        file_content_type = file.content_type
        file_extension = file.filename.split('.')[-1].lower()
        logging.info(
            f"Validating file: {file.filename}, type: {file_content_type}, extension: {file_extension}")
        if (not (
            file_content_type in Settings.ACCEPTED_FILE_TYPES
            or file_extension in Settings.ACCEPTED_FILE_TYPES
        )):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type for {file.filename}",
            )
    return True
