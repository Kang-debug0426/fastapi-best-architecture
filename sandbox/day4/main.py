from fastapi import FastAPI,Depends
from fastapi import Header # 导入 Header 函数，用于获取请求头中的数据
app = FastAPI()
def verify_token(token:str=Header(...)):#这里的Header(...)表示这个参数是必须的，如
  #果请求头中没有这个参数，FastAPI会自动返回一个400错误
   return token


@app.get("/me")
def get_current_user(token=Depends(verify_token)):
    return {"username": "luchia", "token": token}

def get_db():
    print("数据库连接已打开")
    #这里的yield相当于一个生成器函数，第一次调用时会执行到yield语句，返回yield后面的值，然后暂停执行
    # 等待下一次调用时继续执行yield后面的代码，再次等待下一次调用时继续执行yield后面的代码
    yield {"db": "fake_session"}
    print("数据库连接已关闭")



@app.get("/protect")
def protected(db=Depends(get_db), token= Depends(verify_token)):
    return {"db": db, "token": token}