
from sqlalchemy.ext.asyncio import create_async_engine#导入create_async_engine函数，用于创建异步数据库引擎
from sqlalchemy import text #导入text函数，用于执行原生SQL语句
from sqlalchemy.ext.asyncio import AsyncSession#导入AsyncSession类，用于创建异步数据库会话
from sqlalchemy.orm import sessionmaker#导入sessionmaker函数，用于创建数据库会话工厂'''
import redis

redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True, password="cjk123")

DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/fba"
engine = create_async_engine(DATABASE_URL) #创建一个异步数据库引擎，连接到PostgreSQL数据库。DATABASE_URL是数据库的连接字符串
AsyncSessionLocal=sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)#创建一个数据库会话工厂，使用之前创建的异步数据库引擎，
#指定会话类为AsyncSession，并且设置expire_on_commit为False，这样在提交事务后，数据库对象不会过期，可以继续使用。

