from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    UserCreate,
    TokenResponse,
)


router=APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate, db: AsyncSession=Depends(get_db),):
    
    result=await db.execute(select(User).where(User.email==data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    result=await db.execute(select(User).where(User.username==data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user=User(username=data.username, email=data.email, hashed_password=hash_password(data.password),)
    db.add(user)
    
    await db.commit()
    await db.refresh(user)
    
    return TokenResponse(
        access=create_access_token(str(user.id)),
        refresh=create_refresh_token(str(user.id)),
    )
    

@router.post("/login", response_model=TokenResponse)
async def login(data:LoginRequest, db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(User).where(User.email==data.email))
    
    user=result.scalar_one_or_none()
    # if not user or not verify_password(data.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(data.password, user.hashed_password,):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return TokenResponse(
        access=create_access_token(str(user.id)),
        refresh=create_refresh_token(str(user.id)),
    )


@router.post("/refresh")
async def refresh(data: RefreshRequest):
    payload=decode_token(data.refresh)
    if payload["type"] != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {"access": create_access_token(payload["sub"])}


@router.get("/profile")
async def profile(current_user: User=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_active": current_user.is_active,        
    }
    

@router.get("/me")
async def me(current_user: User=Depends(get_current_user)):
    return current_user