import subprocess
import threading
import webbrowser
import time


def start_frontend():
    subprocess.run(
        ["python", "-m", "http.server", "5500"],
        cwd="frontend"   # 关键：进入frontend目录
    )


def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:5500/index.html")


if __name__ == "__main__":

    # 启动前端服务器
    threading.Thread(target=start_frontend).start()

    # 打开浏览器
    threading.Thread(target=open_browser).start()

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )