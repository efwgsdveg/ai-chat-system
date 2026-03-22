from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from storage.database import get_db
from models.user_model import User

router = APIRouter()


@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):

    exist = db.query(User).filter(User.username == username).first()

    if exist:
        return {"msg": "用户名已存在"}

    user = User(
        username=username,
        password=password
    )

    db.add(user)
    db.commit()

    return {"msg": "注册成功"}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User)\
        .filter(User.username == username,
                User.password == password)\
        .first()

    if not user:
        return {"msg": "登录失败"}

    return {
        "msg": "登录成功",
        "user_id": user.id
    }