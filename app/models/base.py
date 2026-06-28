import uuid

from sqlalchemy import (
    DateTime,
    Boolean,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass

class GenericModel(Base):
    __abstract__ = True
    id=mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,)
    created_at=mapped_column(DateTime(timezone=True), server_default=func.now(),)
    updated_at=mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),)
    is_delete=mapped_column(Boolean, default=False,)
    deleted_at=mapped_column(DateTime(timezone=True), nullable=True,)
    