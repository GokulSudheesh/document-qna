import logging
from bson import ObjectId
from app.core.models.session_model import Session
from motor.core import AgnosticDatabase
from app.crud.base import CRUDBase


class CRUDSession(CRUDBase[Session, None, None]):
    async def create(self, db: AgnosticDatabase) -> Session:  # noqa
        return await self.engine.save(Session())

    async def get_by_id(self, db: AgnosticDatabase, id: str):
        logging.info(f"Retrieving session with ID: {ObjectId(id)}")
        sessions = await self.engine.get_collection(Session).aggregate([
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            },
            {
                "$lookup": {
                    "from": "file",
                    "let": {
                        "file_ids": "$files"
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
                                "created": {
                                    "$toString": "$created"
                                },
                                "file_name": 1,
                                "file_type": 1
                            }
                        }
                    ],
                    "as": "files"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": {
                        "$toString": "$_id"
                    },
                    "created": {
                        "$toString": "$created"
                    },
                    "files": 1,
                    "session_name": 1
                }
            }
        ]).to_list()
        return sessions[0] if sessions else None


session = CRUDSession(Session)
