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
from app.schemas.message import EditMessageSchema, ForwardMessageSchema, MessageCreateSchema, MessageOutSchema

router = APIRouter(prefix="/messages", tags=["Mesages"])


@router.get("{chat_id}/messages", response_model=list(MessageOutSchema))
async def message_list(
    chat_id, 
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
    ):

    result=await db.execute(
        select(Message)
        .where(Message.chat_id==chat_id)
        .limit(50)
    )
    return result.scalars().all()


@router.put("/edit/message/{message_id}")
async def edit_message(
    message_id,
    data: EditMessageSchema,
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    message=await db.get(Message, message_id)
    
    if message.sender_id != current_user.id:
        raise HTTPException(403, "not allowed")
    
    message.content=data.content
    message.is_edited=True
    
    await db.commit()
    
    return message


@router.post("/forward/message/{message_id}")
async def forward_message(
    message_id,
    data: ForwardMessageSchema,
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    
    old_msg=await db.get(Message, message_id)
    
    new_msg=Message(
        chat_id=data.chat_id,
        sender_id=current_user.id,
        content=old_msg.content,
        media_file=old_msg.media_file,
        media_type=old_msg.media_type,        
    )
    
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    
    return new_msg


@router.delete("/delete/{message_id}")
async def delete_message(
    message_id,
    db: AsyncSession=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    message=await db.get(Message, message_id)
    
    if message.sender_id != current_user.id:
        raise HTTPException(403, "not allowed")
    
    await db.delete(message)
    await db.commit()
    
    return {"status":"deleted"}


