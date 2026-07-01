from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class MessageCreateSchema(BaseModel):
    content: Optional[str] = None
    reply_to_id: Optional[UUID] = None

class MessageOutSchema(BaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    content: Optional[str]
    is_edited: bool

    class Config:
        from_attributes = True

class EditMessageSchema(BaseModel):
    content: str

class ForwardMessageSchema(BaseModel):
    chat_id: UUID