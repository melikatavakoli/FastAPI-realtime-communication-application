from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from app.models.base import GenericModel
from app.models.chat import Chat
from app.models.user import User


class Membership(GenericModel):
    __tablename__ = 'chat_memberships'
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    chat_id: Mapped[str] = mapped_column(Integer, ForeignKey('chats.id'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_muted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str | None] = mapped_column(String(50), default=None)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),)
    last_read_message_id: Mapped[str | None] = mapped_column(ForeignKey('messages.id'),)
    muted_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),)
    nickname: Mapped[str | None] = mapped_column(String(100),)
    hide_last_seen_for_this_chat: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped["User"] = relationship("User", back_populates="memberships")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="membership")
    last_read_message_id: Mapped["Message"] = relationship("Message", back_populates="memberships")