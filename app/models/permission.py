from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.chat import Chat
    
from app.models.base import GenericModel

class ChatPermission(GenericModel):
    __tablename__ = "chat_membership"
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("chats.id"))
    role: Mapped[str] = mapped_column(String(50))
    permission: Mapped[str] = mapped_column(String(50))
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="permissions")