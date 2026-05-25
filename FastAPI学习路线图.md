# 后端系统从零长出来的过程

> 不是 FastAPI 功能清单。
> 是一个真实后端系统，一层层演化出来的过程。

---

## 学习结构（必须理解）

```
① sandbox/
   最小机制验证。验证单个技术点本质。
   跑通即止，不是长期项目。

② sandbox/ainotes/        ⭐ 主线成长层
   AI Notes System。
   一个真实业务系统，随着阶段一层层长出来。
   每个中间件因业务需要而出现，不是为了学技术而硬加。

③ fastapi-best-architecture/    企业对照层
   每个阶段结束后，去这里看企业如何实现同样的事情。
   它是"参考答案"，不是主线项目。
```

---

## 核心视角

每一阶段，你都在回答同一个问题：

**"这个请求，现在到了系统的哪一层？"**

```
Browser / curl
    ↓
[阶段1] 整条链路观察（FBA）
    ↓
[阶段2] FastAPI 接收请求，路由分发
    ↓
[阶段3] 请求数据校验与转换（Pydantic）
    ↓
[阶段4] 认证链：JWT 解码 → Redis Session 验证
    ↓
[阶段5] 数据持久化：SQLAlchemy → PostgreSQL
    ↓
[阶段6] 缓存层：Redis 加速读取
    ↓
[阶段7] 异步任务：Celery → RabbitMQ → Worker
    ↓
[阶段8] 流式响应：SSE 打字机输出
    ↓
[阶段9] 企业对照：在 FBA 里加真实功能
```

每个阶段结束，你都能在这张图上多点亮一层。

---

## 学习原则

**系统先于语法**：先进容器观察真实数据，再写代码。

**真实优先**：每个阶段必须连接真实组件，禁止用假数据代替。

**成长优先**：ainotes 从一个文件开始，随着业务需要自然拆分，不要过早企业化。

**对照学习**：每个阶段结束后去 FBA 看企业实现，理解"为什么企业要多加那些层"。

**始终知道自己在哪一层**：每次写代码前，先在上面那张图里指出"我现在在操作哪个箭头"。

---

## 阶段 0：系统已经在跑了（✅ 完成）

**你做了什么**：Docker Compose 拉起所有服务，Swagger 登录成功。

**你看到了什么**：一个完整的企业后端系统，已经在你的机器上运行。

**但你还不知道**：一个登录请求，是怎么从 Swagger 流经 FastAPI → JWT → Redis → PostgreSQL 的。

---

## 阶段 1：进入系统内部，观察真实数据流（✅ 完成）

**你在系统的位置**：不是在写代码，是在观察整条链路。

**你做了什么**：
- 进入 PostgreSQL 容器，查到 sys_user 表，确认 admin 用户存在
- Swagger 登录拿到 JWT
- Redis 找到 `fba:token:{user_id}:{uuid}` 格式的 session key
- DEL key 后同一 token 返回 401，验证了 JWT + Redis 协作机制

**你理解了什么**：JWT 负责"你是谁"，Redis Session 负责"你现在还有没有权限"。

**FBA 对照**：这就是 FBA 的认证链，你亲眼看到它运作了。

---

## 阶段 2：ainotes 有了第一个入口

**你在系统的位置**：请求进入 FastAPI 后，如何被路由到正确的处理函数。

**ainotes 这个阶段长出了什么**：
```
POST /notes        创建笔记（存内存 dict）
GET  /notes        获取所有笔记
GET  /notes/{id}   获取单条笔记
```

**目录结构**：
```
sandbox/ainotes/
└── main.py        # 所有代码在这一个文件里
```

**任务清单**：

**Task 2-1：最小入口**
- [ ] 创建 `sandbox/ainotes/main.py`
- [ ] 写 GET `/` 接口，返回 `{"status": "ainotes 运行中"}`
- [ ] `uvicorn main:app --reload --port 8002` 跑起来
- [ ] 访问 `/docs` 看到 Swagger

**Task 2-2：笔记路由**
- [ ] 加 POST `/notes`，接收 `{"title": "...", "content": "..."}`，存入全局 dict
- [ ] 加 GET `/notes`，返回所有笔记
- [ ] 加 GET `/notes/{id}`，返回单条笔记
- [ ] 用 Swagger 测试，创建笔记后能查到

**Task 2-3：FBA 对照**
- [ ] 去 FBA 找入口文件，数一数有多少个路由，它们怎么被注册进来的
- [ ] 对比：ainotes 一个文件，FBA 嵌套了几层 router？为什么？

**完成标准**：能用 Swagger 创建笔记并查到，能说出 FBA 路由为什么要嵌套多层。

**踩坑记录**：

---

## 阶段 3：数据在入口被校验

**你在系统的位置**：请求数据进入 FastAPI 后，在到达业务逻辑之前，被校验和转换。

**ainotes 这个阶段长出了什么**：
- 笔记标题不能为空，最长 100 字
- 内容不能为空，最长 5000 字
- 错误数据在入口被拦截，返回 422

**任务清单**：

**Task 3-1：没有 Schema 会发生什么**
- [ ] 现在用 `data: dict` 接收，故意传空 title，看接口怎么处理
- [ ] 观察：错误数据进入业务逻辑会怎样

**Task 3-2：加 Schema，错误在入口被拦截**
- [ ] 定义 `NoteCreate(BaseModel)`，加 Field 约束
- [ ] 同样传空 title，看 422 在哪里被拦截
- [ ] 定义 `NoteResponse`（不含内部字段），用 `response_model` 过滤响应

**Task 3-3：FBA 对照**
- [ ] 去看 `backend/app/admin/schema/user.py`，数一数有多少个 Schema 类
- [ ] 理解：为什么请求 Schema 和响应 Schema 要分开

**完成标准**：传空 title 返回 422，能说出 Schema 在系统里扮演什么角色。

**踩坑记录**：

---

## 阶段 4：系统知道"你是谁"

**你在系统的位置**：请求如何证明自己的身份？JWT 和 Redis 为什么要配合使用？

**ainotes 这个阶段长出了什么**：
- 用户注册 / 登录接口
- JWT + Redis Session 认证
- 笔记属于某个用户，只有本人能看

**任务清单**：

**Task 4-1：只用 JWT，发现踢下线问题**
- [ ] 加 POST `/auth/register` 和 POST `/auth/login`
- [ ] 登录返回 JWT token
- [ ] GET `/notes` 需要 token 才能访问
- [ ] 思考：JWT 有效期没到，怎么让它失效？

**Task 4-2：加 Redis Session，解决踢下线**
- [ ] 登录时写 Redis session（连接 fba_redis 容器）
- [ ] 认证时验证 Redis session
- [ ] 加 DELETE `/auth/logout`，删 Redis key
- [ ] 验证：logout 后同一 token 返回 401

**Task 4-3：FBA 对照**
- [ ] 去看 `backend/common/security/jwt.py`，找 JWT 生成和解码
- [ ] 搜 `redis_client.set`，找登录时写 session 的位置
- [ ] 对比：FBA 的认证链比你的多了什么？

**完成标准**：能实现登录、认证、踢下线，能说出 JWT 和 Redis Session 各自的职责。

**踩坑记录**：

---

## 阶段 5：数据真正活下来

**你在系统的位置**：通过认证后，业务逻辑要操作数据库。

**ainotes 这个阶段长出了什么**：
- 笔记存入 PostgreSQL（连接 fba_postgres 容器）
- 重启不丢失
- 去掉 dict，换成真实数据库

**目录结构（这时候才拆文件）**：
```
sandbox/ainotes/
├── main.py
├── database.py    # 数据库连接
├── models.py      # SQLAlchemy 表定义
├── schemas.py     # Pydantic Schema
└── routers/
    ├── auth.py
    └── notes.py
```

**数据库表**：
```sql
users  (id, username, email, hashed_password, created_at)
notes  (id, user_id, title, content, summary, created_at, updated_at)
```

**任务清单**：

**Task 5-1：连上数据库**
- [ ] `database.py`，`create_async_engine` 连接 fba_postgres
- [ ] 执行 `SELECT 1`，确认连通

**Task 5-2：定义 Model，建真实的表**
- [ ] 定义 `User` 和 `Note` 表
- [ ] `Base.metadata.create_all` 建表
- [ ] 去 Navicat 看到新表

**Task 5-3：CRUD 真实写入**
- [ ] POST `/notes` → 写入 PostgreSQL → Navicat 验证数据存在
- [ ] GET `/notes` → 从 PostgreSQL 读
- [ ] DELETE `/notes/{id}` → Navicat 验证数据消失

**Task 5-4：FBA 对照**
- [ ] 看 `backend/app/admin/model/sys_user.py` 和 `backend/app/admin/crud/crud_user.py`
- [ ] 对比：你把 CRUD 写在路由函数里，FBA 分了 model / crud / service 三层
- [ ] 思考：如果业务逻辑变复杂，你的写法会出现什么问题？

**完成标准**：重启 ainotes 后笔记数据还在，能说出为什么 FBA 要分三层。

**踩坑记录**：

---

## 阶段 6：系统变快了

**你在系统的位置**：数据库查询结果，在返回给客户端之前，可以被缓存起来。

**ainotes 这个阶段长出了什么**：
- 笔记列表加 Redis 缓存（连接 fba_redis 容器）
- 写入新笔记后自动清缓存

**任务清单**：

**Task 6-1：观察缓存效果**
- [ ] GET `/notes` 加日志，打印"查询数据库"
- [ ] 第一次请求：打印日志，查数据库，结果存 Redis（TTL 60秒）
- [ ] 第二次请求：不打印日志，直接从 Redis 取
- [ ] redis-cli 看 key 存在，等 60 秒后消失

**Task 6-2：缓存失效问题**
- [ ] POST 一条新笔记后，GET 列表还是返回旧数据（缓存没更新）
- [ ] 修复：写入后主动删除缓存 key
- [ ] FBA 对照：搜 `redis_client.delete`，看企业在哪些地方清缓存

**完成标准**：能演示缓存命中和缓存失效，能说出 Redis 缓存解决了什么问题。

**踩坑记录**：

---

## 阶段 7：系统不再让用户等

**你在系统的位置**：AI 摘要生成太慢，不能阻塞请求。

**ainotes 这个阶段长出了什么**：
- 创建笔记后触发 Celery 任务：模拟 AI 生成摘要（sleep 3秒）
- 接口立刻返回，不等 AI 处理完
- 摘要生成后写回数据库

**目录结构（加了 Celery）**：
```
sandbox/ainotes/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── celery_app.py  # Celery 实例
├── tasks.py       # Celery 任务定义
└── routers/
    ├── auth.py
    └── notes.py
```

**任务清单**：

**Task 7-1：没有异步任务会怎样**
- [ ] 在 POST `/notes` 里加 `time.sleep(5)`，模拟 AI 处理
- [ ] 用 Swagger 创建笔记，感受 5 秒等待
- [ ] 思考：100 个用户同时创建笔记会怎样？

**Task 7-2：Celery 异步处理**
- [ ] 配置 Celery，broker 用 fba_rabbitmq，backend 用 fba_redis
- [ ] 写 `generate_summary` task：sleep 3秒，写摘要回数据库
- [ ] POST `/notes` 改为：存笔记 → 触发任务 → 立刻返回
- [ ] 打开 `http://localhost:8555`（Flower），看任务流动

**Task 7-3：FBA 对照**
- [ ] 去 FBA 找 Celery 任务定义，看企业如何组织异步任务
- [ ] 对比：你的 tasks.py 和 FBA 的任务组织有什么差距？

**完成标准**：创建笔记立刻返回，3秒后 Navicat 里能看到摘要写入，能说出 Celery 解决了什么问题。

**踩坑记录**：

---

## 阶段 8：AI 回答实时出现

**你在系统的位置**：数据如何边生成边发送。

**ainotes 这个阶段长出了什么**：
- GET `/notes/{id}/summary/stream` 接口
- SSE 流式返回摘要内容，逐字出现
- 打字机效果

**任务清单**：

**Task 8-1：最小流式响应**
- [ ] `StreamingResponse`，每 0.1 秒 yield 一个字
- [ ] 浏览器访问，看到字一个个出现

**Task 8-2：标准 SSE 格式**
- [ ] 改造为 `data: {content}\n\n` 格式
- [ ] 结束时发 `data: [DONE]\n\n`

**Task 8-3：ainotes 的流式摘要**
- [ ] GET `/notes/{id}/summary/stream`，从数据库取摘要，逐字流式返回
- [ ] 理解：为什么 AI 项目里 SSE 是必须的，不是可选的

**Task 8-4：FBA 对照**
- [ ] 去 FBA 搜 `StreamingResponse`，看企业如何实现流式接口

**完成标准**：浏览器访问流式接口，看到打字机效果，能说出 SSE 和普通接口的区别。

**踩坑记录**：

---

## 阶段 9：企业对照实战

**你在系统的位置**：你已经理解了整条链路，现在进入 FBA，加一个完整模块。

**目标**：在 FBA 里新增"个人笔记"模块，按企业分层实现。

**任务清单**：

**Task 9-1：读懂一个已有模块**
- [ ] 把 sys_user 的 model / schema / crud / service / api 全部读一遍
- [ ] 能解释每一层的职责
- [ ] 对比：ainotes 的写法 vs FBA 的写法，差距在哪里？

**Task 9-2：在 FBA 里加"个人笔记"模块**
- [ ] `backend/app/admin/notes/` 按企业分层实现
- [ ] CRUD + 分页 + 权限
- [ ] 注册到主路由，Swagger 测试

**验收标准**：
- [ ] 能画出登录请求的完整调用链
- [ ] 能在 FBA 里找到任意 bug 并说出它在哪一层
- [ ] 能独立加新接口不破坏现有功能

---

## 阶段总览

| 阶段 | 系统层 | ainotes 长出了什么 | FBA 对照点 | 状态 |
|------|--------|-------------------|-----------|------|
| 0 | 整个系统 | — | Docker Compose 跑通 | ✅ |
| 1 | 整条链路 | — | JWT + Redis 认证链 | ✅ |
| 2 | 路由层 | 笔记 CRUD（内存） | 路由组织方式 | [ ] |
| 3 | 入口校验 | Schema 校验 | Schema 分层 | [ ] |
| 4 | 认证链 | JWT + Redis Session | 认证链实现 | [ ] |
| 5 | 数据持久化 | PostgreSQL 存储 | model/crud/service 三层 | [ ] |
| 6 | 缓存层 | Redis 缓存 | 缓存清理策略 | [ ] |
| 7 | 异步任务 | Celery AI 摘要 | 任务组织方式 | [ ] |
| 8 | 流式响应 | SSE 打字机 | StreamingResponse | [ ] |
| 9 | 企业实战 | — | 在 FBA 加完整模块 | [ ] |

*最后更新：2026-05-24*
