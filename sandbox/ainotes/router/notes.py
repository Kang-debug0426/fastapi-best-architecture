
from fastapi import Depends, APIRouter
from sqlalchemy import text
import json
import redis
from database import AsyncSessionLocal
from model import Note
from schemas import NoteCreate, NoteResponse
from router.auth import verify_token

redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True, password="cjk123")

router = APIRouter()

@router.post("/notes", response_model=NoteResponse)
async def create_item(note: NoteCreate):
    async with AsyncSessionLocal() as session:
        new_note = Note(title=note.title, content=note.content)
        session.add(new_note)
        await session.commit()
        redis_client.delete("ainotes:notes:all")#创建新笔记后，删除缓存中的所有笔记，确保缓存与数据库保持一致。
        await session.refresh(new_note)
    return new_note


@router.get("/notes", response_model=list[NoteResponse])
async def get_note(username: str = Depends(verify_token)):
    cached = redis_client.get("ainotes:notes:all")
    if cached:
        return json.loads(cached)#这是把从Redis缓存中获取的字符串类型的值转换成Python对象。json.loads()函数接受一个字符串类型的参数
    #，并返回一个对应的Python对象。在这个例子中，我们把从Redis缓存中获取的JSON字符串转换成一个Python列表，然后返回给客户端。

    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT id,title,content FROM notes"))
        rows = result.fetchall()
        notes = [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]

    redis_client.set("ainotes:notes:all", json.dumps(notes), ex=60)
    return notes

