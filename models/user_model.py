from sqlalchemy import Column, Integer, String
from storage.database import Base


# =========================
# 用户表
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)  # 用户名唯一
    password = Column(String(100))              # 密码