from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import GenericModel
from app.models.user import User


class Profile(GenericModel):
    __tablename__ = 'profiles'
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    website: Mapped[str] = mapped_column(String(200), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="profile")