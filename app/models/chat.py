from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.membership import Membership
    from app.models.user import User
    from app.models.message import Message
    from app.models.settings import ChatSettings
    from app.models.permission import ChatPermission
    
from app.models.base import GenericModel


class Chat(GenericModel):
    __tablename__ = 'chats'
    name: Mapped[str | None] = mapped_column(String(500),)
    username: Mapped[str | None] = mapped_column(String(100), unique=False)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=True)
    chat_type: Mapped[str] = mapped_column(String(50),)
    description: Mapped[str | None] = mapped_column(String(500),)
    creator: Mapped["User"] = relationship("User", back_populates="chats")
    membership: Mapped["Membership"] = relationship("Membership", back_populates="chat", cascade="all, delete-orphan")
    messages: Mapped["Message"] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    settings: Mapped["ChatSettings"] = relationship("ChatSettings", back_populates="chat", cascade="all, delete-orphan")
    permissions: Mapped["ChatPermission"] = relationship("ChatPermission", back_populates="chat", cascade="all, delete-orphan")