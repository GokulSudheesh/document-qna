import logging
from typing import Tuple
from qdrant_client import models
from langchain_core.documents import Document
from app.core.config import Settings
from app.core.models.completion_response import CompletionResponseWithReferences
from app.core.indexers.qdrant import doc_indexer
from app.core.chain.completion import chat_completion


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs).encode("utf-8")


def get_references(extracted_documents: list[Document]) -> list[dict]:
    references = [
        {"file_name": doc.metadata.get(
            "file_name"), "file_id": doc.metadata.get("file_id")}
        for doc in extracted_documents
    ]
    # Remove duplicates
    return [dict(t) for t in {tuple(d.items()) for d in references}]


async def get_similar_documents(query: str, filter: models.Filter) -> Tuple[list[Document] | None, str | None]:
    try:
        retriever = await doc_indexer.get_retriever(
            filter=filter,
            top_k=Settings.NO_OF_CHUNKS
        )
        if not retriever:
            raise ValueError("Failed to initialize document retriever")
        extracted_documents = await retriever.ainvoke(query)
        extracted_text = format_docs(extracted_documents)
        return (extracted_documents, extracted_text)
    except Exception as e:
        logging.error(f"Error while extracting documents: {str(e)}")
        raise RuntimeError(f"Error while extracting documents: {str(e)}")


async def get_chat_response(session_id: str, query: str, chat_history: list[dict] | None = []) -> CompletionResponseWithReferences:
    docs_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.session_id",
                match=models.MatchValue(value=session_id)
            )
        ]
    )
    extracted_documents, extracted_text = await get_similar_documents(query, docs_filter)
    references = get_references(extracted_documents)
    response = await chat_completion.invoke_with_retry(
        query=query,
        context=extracted_text,
        chat_history=chat_history
    )
    return CompletionResponseWithReferences(
        content=response.content,
        usage_metadata=response.usage_metadata,
        references=references
    )
