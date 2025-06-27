import logging
from typing import Tuple
from qdrant_client import models
from langchain_core.documents import Document
from app.core.config import Settings
from app.core.indexers.qdrant import doc_indexer


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


async def delete_indexed_record(*, session_id: str | None = None, file_id: str | None = None) -> bool:
    try:
        filter_conditions = []
        if session_id:
            filter_conditions.append(
                models.FieldCondition(
                    key="metadata.session_id",
                    match=models.MatchValue(value=session_id)
                )
            )
        if file_id:
            filter_conditions.append(
                models.FieldCondition(
                    key="metadata.file_id",
                    match=models.MatchValue(value=file_id)
                )
            )
        filter = models.Filter(must=filter_conditions)

        return await doc_indexer.delete_record(filter=filter)
    except Exception as e:
        logging.error(f"Error while deleting record: {str(e)}")
        raise RuntimeError(f"Error while deleting record: {str(e)}")
