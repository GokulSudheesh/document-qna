from pydantic import BaseModel


class UsageMetadata(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    content: str
    usage_metadata: UsageMetadata | None = None


class Reference(BaseModel):
    file_name: str
    file_id: str


class CompletionResponseWithReferences(CompletionResponse):
    references: list[Reference] | None = None
