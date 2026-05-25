current_phase: 阶段6 — Redis 缓存
current_task: 缓存基础跑通，GET /notes 已接入 Redis 缓存
status: in_progress

main_project: sandbox/ainotes/    # AI Notes System，主线成长层
fba_role: 企业对照层               # 每阶段结束后对照企业实现

completed:
  - 阶段0: Docker Compose 跑通，Swagger 登录成功（2026-05-22）
  - 阶段1: 整条链路观察完成（2026-05-24）
  - 阶段2: FastAPI 路由层完成（2026-05-24）
  - 阶段3: Pydantic Schema 校验完成（2026-05-24）
  - 阶段4: 认证链完成（2026-05-24）
  - 阶段5: 数据持久化完成（2026-05-25）
    - 连接 fba_postgres，SELECT 1 确认连通
    - 定义 Note 表，Navicat 看到建表成功
    - POST 写入 PostgreSQL，GET 从数据库读
    - 重启后数据还在
  - 文件拆分完成（2026-05-25）
    - main.py / database.py / model.py / schemas.py / router/auth.py / router/notes.py
  - Redis session 调试完成（2026-05-25）
    - 登录写 key，访问验 key，退出删 key，同 token 再访问返回 401

  - 阶段6: Redis 缓存进行中（2026-05-25）
    - GET /notes 加缓存：先查 Redis，命中直接返回，未命中查库后写缓存 TTL 60s
    - ainotes:notes:all key 写入验证成功

pending_questions:
  - JWT + bcrypt + Header 认证这套只跟着敲会了，阶段5连真实数据库时需要结合场景重新讲清楚
    具体困惑：每个函数用法、为什么这样写、真实应用场景

assistant_constraints:
  - 每个任务必须连接真实组件（阶段4起）
  - 阶段5结束后拆文件（现在到时候了）
  - 禁止用 dict/list 假数据代替真实数据库（阶段5起）
  - FBA 是对照层，不是主线，不要让用户长时间读 FBA 源码
