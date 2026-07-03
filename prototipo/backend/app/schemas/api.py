import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    filename: str
    original_filename: str
    content_type: str
    category: str
    metadata_json: str | None
    status: str
    error_message: str | None
    chunk_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class ChatRequest(BaseModel):
    query: str
    messages: list[dict] = []


class ChatToken(BaseModel):
    type: str
    content: str | list | dict


class DeleteResponse(BaseModel):
    message: str
    document_id: UUID
