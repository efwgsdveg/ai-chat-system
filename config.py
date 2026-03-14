import os
from dotenv import load_dotenv

load_dotenv()

QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY")
QIANFAN_URL = "https://qianfan.baidubce.com/v2/chat/completions"
QIANFAN_MODEL = "ernie-4.5-turbo-32k"