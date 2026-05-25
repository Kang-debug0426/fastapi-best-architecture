from fastapi import FastAPI
from routers import users      # 导入 routers 包里的 users 模块
from routers import items      # 导入 routers 包里的 items 模块

app = FastAPI()

app.include_router(users.router)   # 把 users.router 挂到 app 上
app.include_router(items.router)   # 把 items.router 挂到 app 上
