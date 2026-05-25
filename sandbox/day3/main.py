from fastapi import FastAPI
from schemas import UserCreate, UserResponse

app=FastAPI()


@app.post('/users', response_model=UserResponse)

def create_user(user:UserCreate):
    #这里的user是一个UserCreate类型的对象，FastAPI会自动把请求体中的数据转换成UserCreate类型的对象
    #我们这里直接返回一个UserResponse类型的对象，FastAPI会自动把这个对象转换成JSON格式的响应体
    return UserResponse(id=1, username=user.username)