from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    truncate_error=True
)
ALGORITHM=settings.JWT_ALGORITHM

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str)->bool:
    return pwd_context.verify(password, hashed)

def create_access_token(subject: str):
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={
        "sub": subject,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(subject: str):
    expire=datetime.now(timezone.utc)+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload={
        "sub": subject,
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])