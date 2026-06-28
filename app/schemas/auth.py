from pydantic import BaseModel, EmailStr

class LoginAttempt(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access: str
    refresh: str
    
class RefreshRequest(BaseModel):
    refresh: str
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str