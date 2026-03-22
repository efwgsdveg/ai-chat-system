import subprocess
import threading
import webbrowser
import time


# 启动前端服务（静态页面）
def start_frontend():
    subprocess.run(
        ["python", "-m", "http.server", "5500"],
        cwd="frontend"
    )


# 自动打开浏览器
def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:5500/index.html")


if __name__ == "__main__":

    # 启动前端
    threading.Thread(target=start_frontend).start()

    # 打开浏览器
    threading.Thread(target=open_browser).start()

    import uvicorn

    # 启动后端
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )