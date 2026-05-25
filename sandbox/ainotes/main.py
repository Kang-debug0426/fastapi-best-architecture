import uvicorn
from fastapi import FastAPI,HTTPException,Header,Depends
from pydantic import BaseModel
from sqlalchemy import text
from database import  engine
from model import Base,Note
from router import auth, notes
app=FastAPI()
app.include_router(auth.router)
app.include_router(notes.router)

@app.on_event("startup")#这是一个事件处理器，用于在应用启动时执行一些初始化操作。我们使用它来测试数据库连接是否成功。
async def startup():
    async with engine.connect() as conn:
          await conn.execute(text("SELECT 1"))
          print("数据库连接成功")
    async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)
          print("数据库表创建成功")


@app.get("/")
async def root():
    return {"status": "ainotes 运行中"}


