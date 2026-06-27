from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User


oauth2_schema=OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = (oauth2_schema),):
    try:
        payload=decode_token(token)
    except JWTError:
        raise HTTPException(401, "Invlid token",)
    user=await db.get(User, payload["sub"],)
    if user is None:
        raise HTTPException(401, "User not found",)
    return user

