from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 数据库连接地址
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/ai_chat"

# 创建引擎
engine = create_engine(DATABASE_URL)

# 创建Session工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ORM基类
Base = declarative_base()