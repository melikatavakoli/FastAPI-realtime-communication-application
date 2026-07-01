from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.chat import Chat
from app.models.membership import Membership
from app.models.user import User
from app.models.message import Message

from app.schemas.chat import (
    ChatCreateSchema,
    ChatOutSchema,
    AddMemberSchema,
)
from app.schemas.message import MessageCreateSchema, MessageOutSchema

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.get("chat/users/", response_model=list[ChatOutSchema])
async def my_chats(
    db:AsyncSession=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    result=await db.execute(
        select(Chat).join(Chat.membership).where(
            Membership.user_id==current_user.id,
            Membership.is_active==True
        )
    )
    return result.scalars().all()


@router.post("create/chat/", response_model=ChatOutSchema)
async def create_chat(
    data:ChatCreateSchema,
    db: AsyncSession=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    chat=Chat(
        name=data.name,
        chat_type=data.chat_type,
        is_private=data.is_private,
        description=data.description,
        username=data.username,
        creator_id=data.creator_id,
    )
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


@router.post("/{chat_id}/add/members")
async def add_members_chat(
    chat_id,
    data: AddMemberSchema,
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    chat=await db.get(Chat, chat_id)

    if chat.creator_id != current_user.id:
        raise HTTPException(403, "only admin can add members")
    membership=Membership(
        chat_id=chat_id,
        user_id=data.user_id,
        is_active=True,
    )
    db.add(membership)
    await db.commit()
    return {"status": "member added"}


@router.delete("/remove/member/{chat_id}/{user_id}")
async def remove_member_chat(
    chat_id,
    user_id,
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    chat=await db.get(Chat, chat_id)
    
    if chat.creator_id != current_user.id:
        raise HTTPException(403, "only admin can remove members")
    
    result=await db.execute(
        select(Membership).where(
            Membership.chat_id ==chat_id ,
            Membership.user_id==user_id
        )
    )
    
    membership=result.scalar_one_or_none()
    if membership:
        await db.delete(membership)
        await db.commit()
        
    return {"status": "member removed"}


@router.post("/leave/chat/{chat_id}")
async def leave_chat(
    chat_id,
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    result=await db.execute(
        select(Membership).where(
            Membership.chat_id==chat_id,
            Membership.user_id==current_user.id,
        )
    )
    
    member=result.scalar_one_or_none()
    
    if member:
        await db.delete(member)
        await db.commit()
        
    return {"status":"left chat"}