from fastapi import FastAPI
from api.chat_api import router as chat_router
from api.auth_api import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from storage.database import engine, Base

# 创建FastAPI应用
app = FastAPI(
    title="AI聊天API",
    version="1.0"
)

# 自动创建数据库表
Base.metadata.create_all(bind=engine)

# 允许跨域（前端调用必须）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(chat_router)