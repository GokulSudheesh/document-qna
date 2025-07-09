import json
from bson import ObjectId
from qdrant_client import models
from app import crud
from app.core.config import Settings
from app.core.models.chat_model import ChatModel, TransformedChatModel
from app.core.models.completion_model import CompletionResponseWithReferences
from app.core.chain.chat_completion import chat_completion
from app.core.chain.other_completion import session_name_completion
from typing import AsyncGenerator, Any, List
from motor.core import AgnosticDatabase
from app.core.models.enum import MessageRole
from app.core.models.session_model import Session, UpdateSession
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
    chat_history.extend([
        TransformedChatModel(
            role=MessageRole.USER,
            content=query
        ),
        TransformedChatModel(
            role=MessageRole.ASSISTANT,
            content=response.content
        )
    ])
    if (len(chat_history) % Settings.SESSION_NAME_UPDATE_THRESHOLD == 2):
        await update_session_name(db, session, chat_history=chat_history)
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
    response_id = ObjectId()
    async for chunk in chat_completion.astream_with_retry(
        query=query,
        context=extracted_text,
        chat_history=chat_history
    ):
        message += chunk
        message_data = {"id": str(response_id), "message": chunk}
        yield f"event: {Settings.CHAT_STREAM_MESSAGE_EVENT}\ndata: {json.dumps(message_data)}\n\n"
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
            id=response_id,
            session_id=session,
            role=MessageRole.ASSISTANT,
            message=message,
            references=[ObjectId(reference["file_id"])
                        for reference in references]
        )
    )
    chat_history.extend([
        TransformedChatModel(
            role=MessageRole.USER,
            content=query
        ),
        TransformedChatModel(
            role=MessageRole.ASSISTANT,
            content=message
        )
    ])
    if (len(chat_history) % Settings.SESSION_NAME_UPDATE_THRESHOLD == 2):
        await update_session_name(db, session, chat_history=chat_history)
    references_data = {"id": str(response_id), "references": references}
    yield f"event: {Settings.CHAT_STREAM_REFERENCES_EVENT}\ndata: {json.dumps(references_data)}\n\n"


async def update_session_name(db: AgnosticDatabase, session: Session, chat_history: List[TransformedChatModel] | None = []) -> Session:
    session_name = await session_name_completion.invoke_with_retry(chat_history=chat_history)
    logging.info(f"Updating session name to: {session_name}")
    new_session_data = UpdateSession(
        session_name=session_name,
    )
    return await crud.session.update(db, db_obj=session, obj_in=new_session_data)
