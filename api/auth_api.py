from fastapi import APIRouter
from storage.database import SessionLocal
from models.user_model import User

router = APIRouter()

@router.post("/register")
def register(username: str, password: str):

    db = SessionLocal()

    exist = db.query(User).filter(User.username == username).first()

    if exist:
        db.close()
        return {"msg": "用户名已存在"}

    user = User(
        username=username,
        password=password
    )

    db.add(user)
    db.commit()
    db.close()

    return {"msg": "注册成功"}

@router.post("/login")
def login(username: str, password: str):

    db = SessionLocal()

    user = db.query(User)\
        .filter(User.username == username,
                User.password == password)\
        .first()

    db.close()

    if not user:
        return {"msg": "登录失败"}

    return {
        "msg": "登录成功",
        "user_id": user.id
    }