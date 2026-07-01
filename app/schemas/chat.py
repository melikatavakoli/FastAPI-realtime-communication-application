from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

from app.utils.types import ChatType

class ChatCreateSchema(BaseModel):
    name: Optional[str] = None
    chat_type: ChatType
    is_private: bool = True
    description: Optional[str] = None
    username: Optional[str] = None
    

class ChatOutSchema(BaseModel):
    id: UUID
    name: Optional[str]
    chat_type: str
    is_private: bool
    description: Optional[str]

    class Config:
        from_attributes = True
        
class AddMemberSchema(BaseModel):
    user_id: UUID