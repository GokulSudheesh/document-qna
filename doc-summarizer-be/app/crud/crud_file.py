from typing import List

from app.core.config import Settings
from app.core.models.file import ExtractedFile, FileModel
from motor.core import AgnosticDatabase
from app.core.models.session import Session
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder


class CRUDFile(CRUDBase[FileModel, None, None]):
    async def create_multi(self, db: AgnosticDatabase, *, obj_in: List[ExtractedFile], session_obj: Session) -> List[FileModel]:  # noqa
        obj_in = [FileModel(id=file["id"], file_name=file["file_name"],
                            file_type=file["file_type"], session_id=session_obj) for file in obj_in]
        # Extend the session's files with the new file IDs
        session_obj.files.extend(file.id for file in obj_in)
        obj_in_data = jsonable_encoder(obj_in)
        db_objs = [self.model(**data) for data in obj_in_data]  # type: ignore
        return await self.engine.save_all(db_objs)

    async def get_multi(self, session: Session, db: AgnosticDatabase, *, page: int = 0, page_break: bool = False):
        offset = [{"$limit": Settings.MULTI_MAX},
                  {"$skip": page * Settings.MULTI_MAX}] if page_break else []

        files = await self.engine.get_collection(FileModel).aggregate([
            {"$match": {"session_id": session.id}},
            *offset,
            {
                "$project":
                    {
                        "_id": 0,
                        "id": {
                            "$toString": "$_id"
                        },
                        "file_name": 1,
                        "file_type": 1,
                        "session_id": {
                            "$toString": "$session_id"
                        },
                    }
            },
        ]).to_list()
        return files


file = CRUDFile(FileModel)
