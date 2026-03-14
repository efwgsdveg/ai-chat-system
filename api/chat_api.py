from fastapi import APIRouter
from models.chat_model import ChatRequest, ChatMessage
from services.llm_service import call_qianfan
from storage.database import SessionLocal
from sqlalchemy import text
import uuid

router = APIRouter()


# =========================
# 用户注册
# =========================
@router.post("/register")
def register(username: str, password: str):

    db = SessionLocal()

    try:

        db.execute(
            text("INSERT INTO users (username,password) VALUES (:u,:p)"),
            {"u": username, "p": password}
        )

        db.commit()

        return {
            "success": True,
            "msg": "注册成功"
        }

    except:

        return {
            "success": False,
            "msg": "用户名已存在"
        }

    finally:
        db.close()


# =========================
# 用户登录
# =========================
@router.post("/login")
def login(username: str, password: str):

    db = SessionLocal()

    user = db.execute(
        text("SELECT id FROM users WHERE username=:u AND password=:p"),
        {"u": username, "p": password}
    ).fetchone()

    db.close()

    if user:

        session_id = str(uuid.uuid4())

        return {
            "success": True,
            "msg": "登录成功",
            "user_id": user[0],
            "session_id": session_id
        }

    else:

        return {
            "success": False,
            "msg": "用户名或密码错误"
        }


# =========================
# AI聊天
# =========================
@router.post("/chat")
def chat(request: ChatRequest):

    db = SessionLocal()

    user_msg = ChatMessage(
        session_id=request.session_id,
        role="user",
        content=request.message
    )

    db.add(user_msg)
    db.commit()

    history = db.query(ChatMessage)\
        .filter(ChatMessage.session_id == request.session_id)\
        .all()

    messages = [
        {"role": m.role, "content": m.content}
        for m in history
    ]

    ai_reply = call_qianfan(messages)

    ai_msg = ChatMessage(
        session_id=request.session_id,
        role="assistant",
        content=ai_reply
    )

    db.add(ai_msg)
    db.commit()

    db.close()

    return {
        "session_id": request.session_id,
        "user_message": request.message,
        "ai_reply": ai_reply
    }


# =========================
# 聊天历史
# =========================
@router.get("/history/{session_id}")
def get_history(session_id: str):

    db = SessionLocal()

    records = db.query(ChatMessage)\
        .filter(ChatMessage.session_id == session_id)\
        .all()

    db.close()

    return [
        {
            "role": r.role,
            "content": r.content
        }
        for r in records
    ]
@router.get("/sessions/{user_id}")
def get_sessions(user_id: int):

    db = SessionLocal()

    sessions = db.query(ChatMessage.session_id)\
        .distinct()\
        .all()

    result = []

    for s in sessions:

        first_msg = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == s[0])\
            .first()

        title = first_msg.content[:15] if first_msg else "新聊天"

        result.append({
            "session_id": s[0],
            "title": title
        })

    db.close()

    return result

@router.delete("/session/{session_id}")
def delete_session(session_id: str):

    db = SessionLocal()

    db.query(ChatMessage)\
        .filter(ChatMessage.session_id == session_id)\
        .delete()

    db.commit()
    db.close()

    return {"msg":"删除成功"}