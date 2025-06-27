from typing import List
from app.core.models.chat_model import ChatModel, TransformedChatModel
from app.core.models.chat_response import ChatHistoryItem
from app.core.models.session_model import Session
from app.crud.base import CRUDBase
from motor.core import AgnosticDatabase

from app.core.config import Settings


class CRUDChat(CRUDBase[ChatModel, None, None]):
    async def get_transformed_chat_history(self, db: AgnosticDatabase, *, session: Session) -> List[TransformedChatModel]:
        chat_history = await self.engine.get_collection(ChatModel).aggregate(
            [
                {"$match": {"session_id": session.id}},
                {
                    "$project":
                    {
                        "_id": 0,
                        "role": 1,
                        "content": "$message",
                    }
                }
            ]).to_list()
        return chat_history

    async def get_multi(self, db: AgnosticDatabase, *, session: Session, page: int = 0, page_break: bool = False) -> List[ChatHistoryItem]:  # noqa
        offset = [{"$limit": Settings.MULTI_MAX},
                  {"$skip": page * Settings.MULTI_MAX}] if page_break else []
        chat_history = await self.engine.get_collection(ChatModel).aggregate(
            [
                {"$match": {"session_id": session.id}},
                *offset,
                # Transform references field to ensure references is always an array before the lookup
                {
                    "$addFields": {
                        "references": {
                            "$cond": {
                                "if": {
                                    "$ne": [{"$type": "$references"}, "array"]
                                },
                                "then": [],
                                "else": "$references"
                            }
                        }
                    }
                },
                {
                    "$lookup": {
                        "from": "file",
                        "let": {
                            "file_ids": "$references"
                        },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$in": [
                                            "$_id",
                                            "$$file_ids"
                                        ]
                                    }
                                }
                            },
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": {
                                        "$toString": "$_id"
                                    },
                                    "file_name": 1,
                                }
                            }
                        ],
                        "as": "references"
                    }
                },
                # Ensure references is an array or None
                {
                    "$addFields": {
                        "references": {
                            "$cond": {
                                "if": {
                                    "$eq": [{"$size": "$references"}, 0]
                                },
                                "then": None,
                                "else": "$references"
                            }
                        }
                    }
                },
                {
                    "$project":
                    {
                        "_id": 0,
                        "id": {"$toString": "$_id"},
                        "created": {"$toString": "$created"},
                        "session_id": {"$toString": "$session_id"},
                        "role": 1,
                        "message": 1,
                        "references": 1
                    }
                }
            ]).to_list()
        return chat_history


chat = CRUDChat(ChatModel)
