from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.chat_model import ChatRequest, ChatMessage
from services.llm_service import call_qianfan
from storage.database import get_db

router = APIRouter()


# =========================
# AI聊天
# =========================
@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    user_msg = ChatMessage(
        user_id=request.user_id,
        session_id=request.session_id,
        role="user",
        content=request.message
    )

    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    history = db.query(ChatMessage)\
        .filter(ChatMessage.session_id == request.session_id,
                ChatMessage.user_id == request.user_id )\
        .order_by(ChatMessage.id)\
        .all()

    messages = [
        {"role": m.role, "content": m.content}
        for m in history
    ]

    ai_reply = call_qianfan(messages)

    ai_msg = ChatMessage(
        user_id=request.user_id,
        session_id=request.session_id,
        role="assistant",
        content=ai_reply
    )

    db.add(ai_msg)
    db.commit()

    return {
        "session_id": request.session_id,
        "user_message": request.message,
        "ai_reply": ai_reply
    }


# =========================
# 聊天历史
# =========================
@router.get("/history/{session_id}")
def get_history(session_id: str, user_id: int, db: Session = Depends(get_db)):

    records = db.query(ChatMessage)\
        .filter(ChatMessage.session_id == session_id,
                ChatMessage.user_id == user_id)\
        .all()

    return [
        {
            "role": r.role,
            "content": r.content
        }
        for r in records
    ]


# =========================
# 会话列表
# =========================
@router.get("/sessions/{user_id}")
def get_sessions(user_id: int, db: Session = Depends(get_db)):

    subquery = db.query(
    ChatMessage.session_id,
    func.max(ChatMessage.id).label("max_id")
    )\
    .filter(ChatMessage.user_id == user_id)\
    .group_by(ChatMessage.session_id)\
    .subquery()

    sessions = db.query(ChatMessage)\
        .join(subquery, ChatMessage.id == subquery.c.max_id)\
        .order_by(ChatMessage.id.desc())\
        .all()

    result = []

    for s in sessions:

        first_msg = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == s.session_id,
                    ChatMessage.user_id == user_id)\
            .order_by(ChatMessage.id)\
            .first()

        title = first_msg.content[:15] if first_msg else "新聊天"

        result.append({
            "session_id": s.session_id,
            "title": title
        })

    return result


# =========================
# 删除会话
# =========================
@router.delete("/session/{session_id}")
def delete_session(session_id: str,user_id: int, db: Session = Depends(get_db)):

    db.query(ChatMessage)\
        .filter(ChatMessage.session_id == session_id,
                ChatMessage.user_id == user_id )\
        .delete()

    db.commit()

    return {"msg": "删除成功"}