from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column

from app.models.base import GenericModel


class User(GenericModel):
    __tablename__='users'
    username=mapped_column(String(100), unique=True, nullable=False,)
    email=mapped_column(String(300), unique=True, nullable=False,)
    hashed_password=mapped_column(String, nullable=False,)
    first_name=mapped_column(String(100), unique=True, nullable=True,)
    last_name=mapped_column(String(100), unique=True, nullable=True,)
    is_active=mapped_column(Boolean, default=True)
    is_staff=mapped_column(Boolean, default=False)
    is_superuser=mapped_column(Boolean, default=False)
    