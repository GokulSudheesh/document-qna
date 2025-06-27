import io
import logging
from typing import List
from odmantic import ObjectId
from fastapi import UploadFile, HTTPException, status
from app.core.config import Settings
import PyPDF2
from docx import Document
from fastapi import HTTPException
from app.core.models.file_response import ExtractedFile
from app.core.models.enum import FileType
from app.core.indexers.qdrant import doc_indexer
import asyncio


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
                detail=f"Unsupported file type for {file.filename}. Supported types are: {', '.join(Settings.ACCEPTED_FILE_TYPES)}",
            )
    return True


async def extract_pdf(file_content: bytes) -> str:
    return await asyncio.to_thread(extract_pdf_sync, file_content)


def extract_pdf_sync(file_content: bytes) -> str:
    file_content = io.BytesIO(file_content)
    content = ""
    pdf_reader = PyPDF2.PdfReader(file_content)
    num_pages = len(pdf_reader.pages)
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        content += page.extract_text()
    return content


async def extract_docx(file_content: bytes) -> str:
    return await asyncio.to_thread(extract_docx_sync, file_content)


def extract_docx_sync(file_content: bytes) -> str:
    doc = Document(io.BytesIO(file_content))
    extracted_text = ""
    for para in doc.paragraphs:
        extracted_text += para.text + "\n"
    return extracted_text


async def extract_txt(file_content: bytes) -> str:
    return await asyncio.to_thread(extract_txt_sync, file_content)


def extract_txt_sync(file_content: bytes) -> str:
    return file_content.decode("utf-8")


async def extract_files(files: List[UploadFile]):
    extracted_file_content = []
    for file in files:
        content = ""
        file_content = await file.read()
        if (file.content_type == FileType.PDF_TYPE):
            content = await extract_pdf(file_content)
        elif (file.content_type == FileType.DOCX_TYPE or file.content_type == FileType.DOC_TYPE):
            content = await extract_docx(file_content)
        elif (file.content_type == FileType.TEXT_TYPE):
            content = await extract_txt(file_content)
        extracted_file_content.append({
            "file_id": str(ObjectId()),
            "file_name": file.filename,
            "file_type": file.content_type,
            "file_size": file.size,
            "content": content,
        })
    # logging.info(f"Extracted {extracted_file_content} files.")
    return extracted_file_content


async def index_files(session_id: str, files: List[UploadFile]) -> List[ExtractedFile]:
    extracted_files = await extract_files(files)
    filtered_files = []
    for extracted_file in extracted_files:
        filtered_files.append({
            "id": extracted_file["file_id"],
            "file_name": extracted_file["file_name"],
            "file_type": extracted_file["file_type"],
            "file_size": extracted_file["file_size"]
        })
        await doc_indexer.index_documents(
            extracted_text=extracted_file['content'],
            meta_data={
                "session_id": session_id,
                "file_id": extracted_file["file_id"],
                "file_name": extracted_file["file_name"],
                "file_type": extracted_file["file_type"],
                "file_size": extracted_file["file_size"]
            }
        )
    return filtered_files
