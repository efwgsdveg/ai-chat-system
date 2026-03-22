import requests
from fastapi import HTTPException
from config import QIANFAN_API_KEY, QIANFAN_URL, QIANFAN_MODEL


# =========================
# 调用千帆大模型
# =========================
def call_qianfan(messages):

    # 请求头
    headers = {
        "Authorization": f"Bearer {QIANFAN_API_KEY}",
        "Content-Type": "application/json"
    }

    # 请求体
    data = {
        "model": QIANFAN_MODEL,
        "messages": messages
    }

    try:
        # 发送请求
        response = requests.post(
            QIANFAN_URL,
            headers=headers,
            json=data,
            timeout=30,
            proxies={"http": None, "https": None}  # 关闭代理
        )

        # 调试信息（可删除）
        print("状态码:", response.status_code)
        print("返回内容:", response.text)

        response.raise_for_status()

        res_json = response.json()

        # 返回AI回复
        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ 千帆调用失败:", str(e))
        raise HTTPException(status_code=500, detail=str(e))