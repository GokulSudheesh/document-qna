from bson import ObjectId
from qdrant_client import models
from app import crud
from app.core.config import Settings
from app.core.models.chat_model import ChatModel, TransformedChatModel
from app.core.models.completion_model import CompletionResponseWithReferences
from app.core.indexers.qdrant import doc_indexer
from app.core.chain.completion import chat_completion
from typing import AsyncGenerator, Any, List
from motor.core import AgnosticDatabase
from app.core.models.enum import MessageRole
from app.core.models.session_model import Session
from app.core.utils.qdrant import get_references, get_similar_documents
import logging


async def get_chat_response(db: AgnosticDatabase, session: Session, query: str, chat_history: List[TransformedChatModel] | None = []) -> CompletionResponseWithReferences:
    session_id = str(session.id)
    docs_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.session_id",
                match=models.MatchValue(value=session_id)
            )
        ]
    )
    extracted_documents, extracted_text = await get_similar_documents(query, docs_filter)
    logging.info(f"Extracted text: {extracted_text}")
    references = get_references(extracted_documents)
    response = await chat_completion.invoke_with_retry(
        query=query,
        context=extracted_text,
        chat_history=chat_history
    )
    await crud.chat.create(
        db,
        obj_in=ChatModel(
            session_id=session,
            role=MessageRole.USER,
            message=query
        )
    )
    await crud.chat.create(
        db,
        obj_in=ChatModel(
            session_id=session,
            role=MessageRole.ASSISTANT,
            message=response.content,
            references=[ObjectId(reference["file_id"])
                        for reference in references]
        )
    )
    return CompletionResponseWithReferences(
        content=response.content,
        usage_metadata=response.usage_metadata,
        references=references
    )


async def get_stream_chat_response(db: AgnosticDatabase, session: Session, query: str, chat_history: List[TransformedChatModel] | None = []) -> AsyncGenerator[str, Any]:
    session_id = str(session.id)
    docs_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.session_id",
                match=models.MatchValue(value=session_id)
            )
        ]
    )
    extracted_documents, extracted_text = await get_similar_documents(query, docs_filter)
    logging.info(f"Extracted text: {extracted_text}")
    references = get_references(extracted_documents)
    message = ""
    async for chunk in chat_completion.astream_with_retry(
        query=query,
        context=extracted_text,
        chat_history=chat_history
    ):
        message += chunk
        yield f"event: {Settings.CHAT_STREAM_MESSAGE_EVENT}\ndata: {chunk}\n\n"
    logging.info(f"Final message: {message}")
    await crud.chat.create(
        db,
        obj_in=ChatModel(
            session_id=session,
            role=MessageRole.USER,
            message=query
        )
    )
    await crud.chat.create(
        db,
        obj_in=ChatModel(
            session_id=session,
            role=MessageRole.ASSISTANT,
            message=message,
            references=[ObjectId(reference["file_id"])
                        for reference in references]
        )
    )
    yield f"event: {Settings.CHAT_STREAM_REFERENCES_EVENT}\ndata: {references}\n\n"
