import asyncio
from uuid import uuid4
from core.indexers.qdrant import doc_indexer
from utils.qdrant import get_chat_response


async def main():
    response = await get_chat_response(
        session_id="92e3b302-36d6-44c0-83a1-6ce89adae2b7",
        query="What is Amazon river often referred to as?",
        chat_history=[]
    )
    print(f"Response: {response.model_dump_json()}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
