from sqlalchemy import Boolean, String, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GenericModel
from app.models.chat import Chat

class ChatSettings(GenericModel):
    __tablename__="chat_settings"
    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id"))
    description: Mapped[str] = mapped_column(Text)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    invite_link: Mapped[str | None] = mapped_column(String(300))
    slow_mode: Mapped[int] = mapped_column(Integer, default=0)
    only_admins_can_send = Mapped[bool] = mapped_column(Boolean, default=False)
    only_admin_can_add_members = Mapped[bool] = mapped_column(Boolean, default=False)
    only_admin_can_pin: Mapped[bool] = mapped_column(Boolean, default=True)
    can_send_media: Mapped[bool] = mapped_column(Boolean, default=True)
    can_send_voice: Mapped[bool] = mapped_column(Boolean, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    subscribers_count: Mapped[int] = mapped_column(Integer, default=0)
    hide_members_list: Mapped[bool] = mapped_column(Boolean, default=False)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="settings")