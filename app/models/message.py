from sqlalchemy import Text, Boolean, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GenericModel
from app.models.chat import Chat
from app.models.membership import Membership
from app.models.user import User

class Message(GenericModel):
    __tablename__ = 'messages'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    voice: Mapped[bytes | None] = mapped_column()
    send_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),)
    reply_to_id: Mapped[str | None] = mapped_column(ForeignKey('messages.id'),)
    forward_from_id: Mapped[str | None] = mapped_column(ForeignKey('messages.id'),)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    can_forward: Mapped[bool] = mapped_column(Boolean, default=True)
    media_file: Mapped[str | None] = mapped_column(String,)
    media_type: Mapped[str | None] = mapped_column(String(50),)
    emoji: Mapped[str | None] = mapped_column(String(50),)
    forwarded_from_user_id: Mapped[str | None] = mapped_column(ForeignKey('users.id'),)
    forwarded_from_chat_id: Mapped[str | None] = mapped_column(ForeignKey('chats.id'),)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    pin_expiry: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True),)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default='now()')
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate='now()')
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chats.id'), nullable=False)
    sender: Mapped["User"] = relationship("User", back_populates="messages")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    memberships: Mapped["Membership"] = relationship("Membership", back_populates="last_read_message_id")
    replies: Mapped["Message"] = relationship("Message", remote_side="Message.id", foreign_keys=[reply_to_id])
    