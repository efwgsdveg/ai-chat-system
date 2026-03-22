from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from storage.database import Base


class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_id:int

id="fix_user_id"
class ChatMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)   # ✅ 新增
    session_id = Column(String(100))
    role = Column(String(20))
    content = Column(Text)