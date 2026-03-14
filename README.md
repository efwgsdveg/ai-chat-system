# AI Chat System

一个基于 FastAPI 构建的 AI 聊天系统，支持用户登录、多会话管理、聊天记录保存等功能。

该项目实现了一个简单的前后端分离 AI 聊天应用：
- 后端使用 FastAPI 提供 REST API
- 前端使用 HTML + JavaScript 调用接口
- 使用 MySQL + SQLAlchemy ORM 存储用户和聊天数据

---

# 技术栈

Backend

- FastAPI
- SQLAlchemy (ORM)
- MySQL
- Uvicorn

Frontend

- HTML
- JavaScript
- Fetch API

---

# 功能

- 用户注册 / 登录
- AI聊天接口
- 聊天记录存储
- 多会话管理
- 删除会话
- 聊天历史查看

---

# 项目结构

```
ai-chat-system
│
├── api                # API接口层
├── models             # 数据库ORM模型
├── services           # 业务逻辑层
├── storage            # 数据库连接配置
├── frontend           # 前端页面
│
├── main.py            # FastAPI入口
├── run.py             # 项目启动脚本
├── config.py          # 项目配置
├── requirements.txt   # Python依赖
└── README.md
```

---

# 数据库配置

项目使用 **MySQL** 数据库，并通过 **SQLAlchemy ORM** 自动创建数据表。

## 1 安装 MySQL

确保本地已安装并启动 MySQL 数据库服务。

默认端口：

```
3306
```

---

## 2 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE ai_chat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 3 配置数据库连接

在 `config.py` 中配置数据库连接，例如：

```python
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ai_chat"
```

参数说明：

| 参数 | 含义 |
|----|----|
| root | MySQL用户名 |
| 123456 | MySQL密码 |
| localhost | 数据库地址 |
| 3306 | 数据库端口 |
| ai_chat | 数据库名称 |

---

## 4 自动创建数据表

项目使用 SQLAlchemy ORM 自动创建数据库表。

在 `main.py` 中：

```python
Base.metadata.create_all(bind=engine)
```

当应用启动时，如果数据库为空，系统会自动创建所有表结构，例如：

- users
- conversations
- messages

无需手动执行 SQL 创建表。

---

# 项目运行

## 1 安装依赖

```
pip install -r requirements.txt
```

## 2 启动服务

```
python run.py
```

或

```
uvicorn main:app --reload
```

---

## 3 访问服务

API 服务地址：

```
http://localhost:8000
```

FastAPI 自动生成的接口文档：

```
http://localhost:8000/docs
```

---

# 项目截图（可选）

可以在这里放系统截图，例如：

- 登录界面
- 聊天界面
- 会话管理界面

---

# License

This project is for learning and demonstration purposes.