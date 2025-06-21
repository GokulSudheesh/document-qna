from pydantic import BaseModel


class DocMetaData(BaseModel):
    file_id: str
    session_id: str
    file_name: str
    file_type: str
