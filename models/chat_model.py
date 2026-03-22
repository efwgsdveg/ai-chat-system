from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from storage.database import Base


# =========================
# 请求数据模型（前端传入）
# =========================
class ChatRequest(BaseModel):
    session_id: str   # 会话ID
    message: str      # 用户输入
    user_id: int      # 当前用户ID


# =========================
# 数据库表：聊天记录
# =========================
class ChatMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)       # 所属用户
    session_id = Column(String(100))# 会话ID
    role = Column(String(20))       # user / assistant
    content = Column(Text)          # 消息内容