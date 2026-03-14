from fastapi import FastAPI
from api.chat_api import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from models import chat_model
from models import user_model
from storage.database import engine, Base

app = FastAPI(
    title="AI聊天API",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)