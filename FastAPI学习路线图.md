# FastAPI 后端源码拆解与实战路线图

## 推荐项目

### 首选：fastapi-practices/fastapi_best_architecture

**仓库地址**：https://github.com/fastapi-practices/fastapi_best_architecture

| 需求 | 匹配度 |
|------|--------|
| FastAPI + MySQL + Redis + Docker | 全部满足，SQLAlchemy 2.0 + Pydantic V2 |
| 规范的分层架构 | 伪三层架构：`api(router)` → `service` → `crud/model` |
| docker-compose 一键拉起 | 完整 `docker-compose.yml`，含 MySQL、Redis、Celery |
| 适合作为 AI 后端模板 | 架构清晰、模块解耦，后续加 LLM 接口非常自然 |

**额外加分项**：
- 内置 RBAC 权限管理、JWT 认证、Celery 异步任务
- 中文文档和社区，遇到问题容易找到帮助
- 使用 Alembic 做数据库迁移（生产级标配）
- 有配套前端 UI 仓库（可选）

### 备选：fastapi-practices/fastapi_sqlalchemy_mysql

**仓库地址**：https://github.com/fastapi-practices/fastapi_sqlalchemy_mysql

同一组织下的**精简版脚手架**，技术栈相同（FastAPI + Pydantic V2 + SQLAlchemy 2.0 + Alembic + MySQL + Redis），功能更少、代码量更小。如果主项目一开始太复杂，可先花 1-2 天看这个精简版理解基本骨架，再切到完整版。

---

## 实战学习路线（每天 5-8 小时，共 12 天）

---

### Day 1：环境拉起 + 项目全貌

**目标**：跑通项目，打开 Swagger 文档页面

**动作**：
1. `git clone` 项目，通读根目录的 `README.md` 和 `docker-compose.yml`
2. 理解 compose 中定义了哪些服务（app、mysql、redis、celery worker）
3. 执行 `docker-compose up -d` 拉起全部服务
4. 浏览器访问 `http://localhost:8000/docs`，确认 Swagger UI 正常加载
5. 用 Swagger 手动调几个接口（如登录、获取用户列表），建立直觉

**重点文件**：
- `docker-compose.yml` — 服务编排
- `.env` 或 `core/conf.py` — 配置管理方式
- `main.py` 或 `app.py` — 应用入口

---

### Day 2：项目结构与路由分发

**目标**：搞清楚一个请求从 URL 到函数的完整路径

**动作**：
1. 画出项目目录树，标注每个文件夹的职责
2. 从 `main.py` 出发，找到 `app = FastAPI()` 和路由注册的位置
3. 追踪一个具体路由（如 `/api/v1/auth/login`），看它如何通过 `APIRouter` → `include_router` 层层挂载
4. 阅读 2-3 个 router 文件，总结路由定义的模式

**核心概念**：
- `APIRouter` 的 `prefix` 和 `tags` 参数
- 路由文件的组织方式（按业务模块分文件）
- `__init__.py` 中的路由汇总注册

---

### Day 3：Pydantic 数据校验 + 响应模型

**目标**：理解请求/响应数据如何被自动校验和序列化

**动作**：
1. 找到 `schema`（或 `schemas`）目录，阅读 3-4 个 schema 文件
2. 对比「请求 Schema」和「响应 Schema」的区别
3. 看路由函数的参数类型标注如何与 Schema 绑定
4. 在 Swagger 中故意传错误数据，观察 422 校验错误的返回格式
5. 自己仿写一个新的 Schema，体会 `Field`、`validator`、`model_config` 的用法

**核心概念**：
- `BaseModel` 继承与字段定义
- `Field(...)` 的校验参数（min_length、ge、regex 等）
- 响应模型 `response_model` 的作用

---

### Day 4：依赖注入（Depends）

**目标**：理解 FastAPI 最核心的设计模式

**动作**：
1. 全局搜索 `Depends(`，收集项目中所有依赖注入的用法
2. 分类整理：
   - 获取数据库 Session 的依赖（`get_db`）
   - 获取当前用户的依赖（`get_current_user`）
   - 权限校验的依赖
3. 追踪一个需要登录的接口，看 `Depends` 链如何层层嵌套
4. 自己写一个简单的依赖（如：从 Header 中提取自定义 token）

**核心概念**：
- 依赖函数 vs 依赖类
- 依赖的嵌套组合
- `yield` 依赖（用于数据库 session 的生命周期管理）

---

### Day 5：SQLAlchemy ORM + CRUD 层

**目标**：掌握数据库操作的完整链路

**动作**：
1. 找到 `model` 目录，阅读 2-3 个数据模型定义（表结构）
2. 找到 `crud` 目录，看基础 CRUD 类如何封装 `session.query` / `session.execute`
3. 追踪一个完整的写操作（如创建用户）：`router → service → crud → model → DB`
4. 阅读 `alembic/` 目录，理解数据库迁移的工作流
5. 尝试自己新增一个表和对应的 CRUD

**核心概念**：
- `DeclarativeBase` 模型定义
- `AsyncSession` 异步数据库操作
- `select()` / `insert()` / `update()` 的 SQLAlchemy 2.0 写法
- Alembic 的 `revision` 和 `upgrade` 命令

---

### Day 6：Redis 缓存集成

**目标**：理解 Redis 在项目中的角色和使用方式

**动作**：
1. 搜索项目中所有 `redis` 相关代码，找到 Redis 客户端的初始化位置
2. 整理 Redis 的使用场景（Token 黑名单、接口限流、缓存热数据）
3. 追踪一个具体的 Redis 读写流程（如 token 存储/校验）
4. 看 Redis 连接是如何通过依赖注入或全局单例提供的
5. 自己写一个简单的缓存逻辑：先查 Redis，miss 则查 DB 并回写

**核心概念**：
- `aioredis` / `redis-py` 异步客户端
- Redis 连接池配置
- Key 的命名规范和 TTL 设置

---

### Day 7：中间件 + 异常处理 + 日志

**目标**：理解请求生命周期中的横切关注点

**动作**：
1. 找到中间件注册的位置，阅读每个中间件的作用（CORS、请求日志、耗时统计等）
2. 找到全局异常处理器，看项目如何统一错误响应格式
3. 阅读日志配置，理解 `loguru` 或 `logging` 的集成方式
4. 在 Swagger 中触发不同类型的错误，观察响应格式的一致性

**核心概念**：
- `@app.middleware("http")` 的执行顺序
- `@app.exception_handler` 自定义异常
- 统一响应格式的设计思路

---

### Day 8：认证与权限（JWT + RBAC）

**目标**：理解生产级认证系统的实现

**动作**：
1. 追踪完整的登录流程：用户名密码 → 校验 → 生成 JWT → 返回 token
2. 追踪 token 校验流程：请求带 token → 解析 → 获取用户 → 注入到路由
3. 阅读 RBAC 权限控制的实现（角色、菜单、权限的关联）
4. 理解 `Depends(get_current_user)` 背后的完整逻辑链

**核心概念**：
- JWT 的签发与验证（`python-jose` 或 `PyJWT`）
- Token 刷新机制
- 基于角色的访问控制

---

### Day 9：Celery 异步任务

**目标**：理解耗时操作如何异步化

**动作**：
1. 找到 Celery 的配置文件和 worker 启动方式
2. 阅读 1-2 个异步任务的定义（如发送邮件、数据导出）
3. 看路由如何触发异步任务并返回 task_id
4. 理解 Celery + Redis（作为 broker）的协作关系

**核心概念**：
- Celery 的 task 定义和调用
- broker（Redis）和 backend 的角色
- 任务状态查询

---

### Day 10-11：AI 接口预演 — 实现流式输出接口

**目标**：在现有架构下，手写一个 SSE 流式输出接口，模拟大模型的打字机效果

#### Day 10 — 基础实现

1. 新建路由模块 `api/v1/ai/chat.py`
2. 实现 `StreamingResponse` 接口：

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter(prefix="/ai", tags=["AI"])


async def fake_llm_stream(prompt: str):
    """模拟大模型的流式输出"""
    response_text = f"你好！你问的是：{prompt}。这是一个模拟的流式回答，每个字会逐个输出。"
    for char in response_text:
        yield f"data: {char}\n\n"
        await asyncio.sleep(0.05)
    yield "data: [DONE]\n\n"


@router.get("/chat/stream")
async def chat_stream(prompt: str):
    return StreamingResponse(
        fake_llm_stream(prompt),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
```

3. 将路由注册到主 app，用浏览器或 `curl` 测试流式效果

#### Day 11 — 进阶整合

1. 为流式接口加上认证（`Depends(get_current_user)`）
2. 加上请求参数的 Pydantic Schema 校验
3. 加上 Redis 对话历史缓存（存储最近 N 轮对话）
4. 预留 `httpx` 调用外部 LLM API 的位置：

```python
import httpx


async def real_llm_stream(prompt: str):
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "https://api.example.com/v1/chat/completions",
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
            },
            headers={"Authorization": "Bearer YOUR_KEY"},
        ) as response:
            async for chunk in response.aiter_lines():
                if chunk.startswith("data: "):
                    yield chunk + "\n\n"
```

---

### Day 12：回顾 + 自建完整模块

**目标**：验证学习成果，独立完成一个完整的业务模块

**动作**：
1. 不看参考，从零新增一个完整模块（如「笔记管理」）：
   - Model（数据表）
   - Schema（请求/响应）
   - CRUD（数据库操作）
   - Service（业务逻辑）
   - Router（路由接口）
2. 包含：分页查询、创建、更新、删除
3. 加上 Redis 缓存热门笔记
4. 加上权限控制（仅作者可编辑）
5. 写完后用 Swagger 完整测试

---

## 学习节奏总览

| 阶段 | 天数 | 核心产出 |
|------|------|---------|
| 环境 + 骨架理解 | Day 1-2 | 能跑通项目，画出架构图 |
| 三大核心机制 | Day 3-5 | 掌握 Pydantic + Depends + SQLAlchemy |
| 基建层 | Day 6-8 | 理解 Redis / 中间件 / 认证的生产级实现 |
| 异步 + AI 预演 | Day 9-11 | 能独立写出流式接口 |
| 综合实战 | Day 12 | 独立完成完整业务模块 |

---

## 完成后的下一步

12 天完成后，你将具备在 FastAPI 架构下独立开发 AI 后端接口的能力，可以直接进入：

- **LangChain + FastAPI**：构建 RAG 应用后端
- **LlamaIndex + FastAPI**：构建知识库问答系统
- **Agent 框架 + FastAPI**：构建多工具调用的 AI Agent 服务

---

## 参考资源

- [fastapi_best_architecture](https://github.com/fastapi-practices/fastapi_best_architecture)
- [fastapi_sqlalchemy_mysql](https://github.com/fastapi-practices/fastapi_sqlalchemy_mysql)
- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [FastAPI 官方文档 - 大型应用结构](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
