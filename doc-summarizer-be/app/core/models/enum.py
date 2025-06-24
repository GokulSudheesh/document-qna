from enum import StrEnum


class FileType(StrEnum):
    TEXT_TYPE = "text/plain"
    PDF_TYPE = "application/pdf"
    DOC_TYPE = "application/msword"
    DOCX_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
