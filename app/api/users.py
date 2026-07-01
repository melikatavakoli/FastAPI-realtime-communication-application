from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserList
from app.utils.paginations import PaginationParam, pagination_param


router=APIRouter(prefix="/users", tags=["Users"])

@router.get("users/list", response_model=list[UserList])
async def user_list(
    db: AsyncSession=Depends(get_db), 
    current_user:User=Depends(get_current_user),
    pagination: PaginationParam=Depends(pagination_param)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="permission denied",
        )
    result=await db.execute(
        select(User)
        .offset(pagination.skip)
        .limit(pagination.limit)
        )
    return result.scalars().all()