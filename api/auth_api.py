from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from storage.database import SessionLocal
from models.user_model import User

# 创建路由对象
router = APIRouter()


# =========================
# 数据库依赖注入
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db   # 提供数据库连接
    finally:
        db.close() # 请求结束关闭连接


# =========================
# 用户注册
# =========================
@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):

    # 查询是否已有该用户名
    exist = db.query(User).filter(User.username == username).first()

    if exist:
        return {"msg": "用户名已存在"}

    # 创建用户对象
    user = User(
        username=username,
        password=password
    )

    # 写入数据库
    db.add(user)
    db.commit()

    return {"msg": "注册成功"}


# =========================
# 用户登录
# =========================
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    # 查询用户
    user = db.query(User)\
        .filter(User.username == username,
                User.password == password)\
        .first()

    # 登录失败
    if not user:
        return {"msg": "登录失败"}

    # 登录成功
    return {
        "msg": "登录成功",
        "user_id": user.id   # 返回用户ID供前端使用
    }