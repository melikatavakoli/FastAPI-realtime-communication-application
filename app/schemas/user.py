from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID


class UserList(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None
    is_staff: bool
    
    model_config = ConfigDict(from_attributes=True)