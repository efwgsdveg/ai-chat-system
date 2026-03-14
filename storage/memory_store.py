from typing import Dict, List

chat_histories: Dict[str, List[dict]] = {}

def get_history(session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

def clear_history(session_id: str):
    if session_id in chat_histories:
        del chat_histories[session_id]