from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GenericModel
from app.models.chat import Chat

class ChatPermission(GenericModel):
    __tablename__ = "chat_membership"
    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id"))
    role: Mapped[str] = mapped_column(String(50))
    permission: Mapped[str] = mapped_column(String(50))
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="permissions")