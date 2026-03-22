# 🧠 AI Chat System（多用户智能对话系统）

## 📌 项目简介

本项目是一个基于 **FastAPI + MySQL + 前端原生页面** 构建的 AI 多轮对话系统，支持用户注册登录、多会话管理以及聊天历史持久化。

系统接入大模型（千帆 API），实现类似 ChatGPT 的对话体验，并支持多用户数据隔离。

---

## 🚀 功能特性

### 👤 用户系统

* 用户注册 / 登录
* 本地存储 user_id 实现登录态
* 多用户数据隔离（核心功能）

### 💬 聊天系统

* 支持多轮对话（上下文记忆）
* 聊天记录持久化（MySQL）
* 自动拼接历史消息发送给大模型

### 📂 会话管理

* 支持多个聊天会话（类似 ChatGPT）
* 会话列表展示
* 会话切换 / 删除
* 自动生成会话标题

### 🧠 AI能力

* 接入千帆大模型 API
* 支持上下文对话
* 实时返回 AI 回复

---

## 🏗️ 项目结构

```
ai-chat-system
│
├── api                # API接口层
│   ├── auth_api.py    # 登录注册接口
│   └── chat_api.py    # 聊天/历史/会话接口
│
├── models             # 数据库模型
│   ├── user_model.py
│   └── chat_model.py
│
├── services           # 业务逻辑
│   └── llm_service.py # 大模型调用
│
├── storage            # 数据库配置
│   └── database.py
│
├── frontend           # 前端页面
│   ├── index.html     # 登录页
│   └── chat.html      # 聊天页
│
├── main.py            # FastAPI入口
├── run.py             # 一键启动脚本
├── config.py          # API配置
├── requirements.txt
└── README.md
```

---

## ⚙️ 技术栈

* **后端**：FastAPI
* **数据库**：MySQL + SQLAlchemy
* **前端**：HTML + CSS + JavaScript（原生）
* **AI接口**：千帆大模型 API
* **运行方式**：uvicorn + 本地HTTP服务

---

## 🧩 核心设计

### 1️⃣ 多用户数据隔离

在 `messages` 表中引入 `user_id` 字段：

```sql
user_id + session_id 共同确定数据归属
```

所有查询均带 user_id 过滤：

```python
.filter(ChatMessage.user_id == user_id)
```

✅ 解决不同用户数据混用问题

---

### 2️⃣ 多会话管理

通过 `session_id` 区分不同对话：

* 每次新建聊天生成新的 session_id
* 同一 session_id 共享上下文
* 支持历史记录回溯

---

### 3️⃣ 上下文对话实现

```python
messages = [
    {"role": m.role, "content": m.content}
    for m in history
]
```

将历史记录拼接后发送给大模型，实现多轮对话。

---

### 4️⃣ 数据库连接管理（依赖注入）

使用 FastAPI Depends 管理数据库生命周期：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🛠️ 环境配置

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

---

### 2️⃣ 配置数据库

修改 `storage/database.py`：

```python
DATABASE_URL = "mysql+pymysql://root:密码@localhost:3306/ai_chat"
```

创建数据库：

```sql
CREATE DATABASE ai_chat;
```

---

### 3️⃣ 配置大模型

修改 `config.py`：

```python
QIANFAN_API_KEY = "你的API_KEY"
QIANFAN_URL = "接口地址"
QIANFAN_MODEL = "模型名称"
```

---

## ▶️ 启动项目

```bash
python run.py
```

启动后：

* 前端：http://localhost:5500
* 后端：http://127.0.0.1:8000

---

## 🧪 使用流程

1. 打开登录页面
2. 注册账号
3. 登录系统
4. 进入聊天界面
5. 开始对话 / 创建新会话

---

## 📈 项目亮点

* ✅ 完整的前后端 AI 应用
* ✅ 多用户数据隔离（工程能力体现）
* ✅ 多会话管理（接近真实产品）
* ✅ 上下文对话实现
* ✅ 使用依赖注入优化数据库管理
* ✅ 具备实际部署和扩展能力

---

## 🔮 可扩展方向

* 接入 RAG（知识库问答）
* 增加 Token 限制 / 截断策略
* 用户权限系统（JWT）
* UI 优化（React / Vue）
* 部署上线（Docker / 云服务器）

---

## 📌 项目说明

本项目用于 AI 应用开发学习与实践，重点在于：

* 后端架构设计
* AI接口集成
* 多用户系统实现

---

## 👨‍💻 作者

个人练习项目，用于实习求职与能力展示。
