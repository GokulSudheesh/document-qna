from pydantic import BaseModel
from app.core.models.enum import FileType
from datetime import datetime
from odmantic import Field, Reference
from app.db.base_class import Base
from app.core.models.session_model import Session


class DocMetaData(BaseModel):
    file_id: str
    session_id: str
    file_name: str
    file_type: str
    file_size: int | None


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class FileModel(Base):
    created: datetime = Field(default_factory=datetime_now_sec)
    file_name: str = Field()
    file_type: FileType = Field()
    file_size: int = Field(default=None)
    session_id: Session = Reference()
