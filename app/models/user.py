from profile import Profile

from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.models.base import GenericModel


class User(GenericModel):
    __tablename__='users'
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False
    )