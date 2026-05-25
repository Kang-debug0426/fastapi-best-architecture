from fastapi  import FastAPI
import uvicorn
app = FastAPI()
@app.get("/hello")
def read_root():
  return {"Hello":"World"}
if __name__ == '__main__':
  uvicorn.run('hello:app',host="127.0.0.1",
              port=8000,reload=True,debug=True)
              
@app.get('/hello/{name}')
def accept(name:str):#这里叫参数类型路径注解
  #我们这里是url参数分类的路径参数模式

  return {"greeting": f"hello {name}"}

@app.post('/user')
def create_user(data: dict):
  return {"receive": data,"status": "ok"}