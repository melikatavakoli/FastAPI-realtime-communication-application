from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.chats import router as chat_router
from app.api.messages import router as message_router
import app.models

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(message_router, prefix="/api/v1")