# NEXT_ACTION.md

阶段6 - Redis 缓存

Task 6-1：给 GET /notes 加缓存
1. 在 notes.py 的 get_note 里，先查 Redis 有没有缓存
2. 有缓存直接返回，没有才查数据库
3. 查完数据库后写入 Redis，设置 TTL 60 秒
4. 用 redis-cli 验证 key 存在，TTL 在倒计时

Task 6-2：验证缓存生效
1. 第一次请求：Redis 没有 → 查数据库 → 写缓存
2. 第二次请求：Redis 有 → 直接返回，不查数据库
3. 在数据库里手动改一条数据，60 秒内再请求，看到的还是旧数据（缓存未过期）
4. 等 60 秒后再请求，看到新数据（缓存过期，重新查库）
