from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.chat_model import ChatRequest, ChatMessage
from services.llm_service import call_qianfan
from storage.database import SessionLocal

router = APIRouter()


# =========================
# 数据库依赖注入
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# AI聊天接口
# =========================
@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    # ---------- 1. 保存用户消息 ----------
    user_msg = ChatMessage(
        user_id=request.user_id,         # 当前用户ID
        session_id=request.session_id,   # 会话ID
        role="user",                     # 角色：用户
        content=request.message          # 用户输入内容
    )

    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)  # 刷新获取数据库生成的数据


    # ---------- 2. 获取历史记录 ----------
    history = db.query(ChatMessage)\
        .filter(
            ChatMessage.session_id == request.session_id,
            ChatMessage.user_id == request.user_id   # 只查当前用户
        )\
        .order_by(ChatMessage.id)\
        .all()


    # ---------- 3. 转换为大模型格式 ----------
    messages = [
        {"role": m.role, "content": m.content}
        for m in history
    ]


    # ---------- 4. 调用大模型 ----------
    ai_reply = call_qianfan(messages)


    # ---------- 5. 保存AI回复 ----------
    ai_msg = ChatMessage(
        user_id=request.user_id,
        session_id=request.session_id,
        role="assistant",   # 角色：AI
        content=ai_reply
    )

    db.add(ai_msg)
    db.commit()


    # ---------- 6. 返回结果 ----------
    return {
        "session_id": request.session_id,
        "user_message": request.message,
        "ai_reply": ai_reply
    }


# =========================
# 获取聊天历史
# =========================
@router.get("/history/{session_id}")
def get_history(session_id: str, user_id: int, db: Session = Depends(get_db)):

    # 查询当前用户该会话的所有记录
    records = db.query(ChatMessage)\
        .filter(
            ChatMessage.session_id == session_id,
            ChatMessage.user_id == user_id
        )\
        .all()

    # 返回前端需要的数据结构
    return [
        {
            "role": r.role,
            "content": r.content
        }
        for r in records
    ]


# =========================
# 获取会话列表
# =========================
@router.get("/sessions/{user_id}")
def get_sessions(user_id: int, db: Session = Depends(get_db)):

    # 子查询：获取每个session最新一条记录
    subquery = db.query(
        ChatMessage.session_id,
        func.max(ChatMessage.id).label("max_id")
    )\
    .filter(ChatMessage.user_id == user_id)\
    .group_by(ChatMessage.session_id)\
    .subquery()


    # 查询最新记录（用于排序）
    sessions = db.query(ChatMessage)\
        .join(subquery, ChatMessage.id == subquery.c.max_id)\
        .order_by(ChatMessage.id.desc())\
        .all()

    result = []

    for s in sessions:

        # 找该session第一条消息作为标题
        first_msg = db.query(ChatMessage)\
            .filter(
                ChatMessage.session_id == s.session_id,
                ChatMessage.user_id == user_id
            )\
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
def delete_session(session_id: str, user_id: int, db: Session = Depends(get_db)):

    # 删除当前用户该会话所有记录
    db.query(ChatMessage)\
        .filter(
            ChatMessage.session_id == session_id,
            ChatMessage.user_id == user_id
        )\
        .delete()

    db.commit()

    return {"msg": "删除成功"}