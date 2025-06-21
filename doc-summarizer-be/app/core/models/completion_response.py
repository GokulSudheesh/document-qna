from pydantic import BaseModel


class CompletionResponse(BaseModel):
    content: str
    usage_metadata: dict | None = None


class Reference(BaseModel):
    file_name: str
    file_id: str


class CompletionResponseWithReferences(CompletionResponse):
    references: list[Reference] | None = None
