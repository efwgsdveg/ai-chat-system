import requests
from fastapi import HTTPException
from config import QIANFAN_API_KEY, QIANFAN_URL, QIANFAN_MODEL

def call_qianfan(messages):

    headers = {
        "Authorization": f"Bearer {QIANFAN_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": QIANFAN_MODEL,
        "messages": messages
    }

    try:
        response = requests.post(QIANFAN_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        res_json = response.json()

        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))