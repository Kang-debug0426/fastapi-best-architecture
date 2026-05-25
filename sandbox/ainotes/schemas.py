from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
  title: str= Field(..., min_length=1, max_length=100)
  content: str=  Field(..., min_length=1, max_length=5000)
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

class LoginRequest(BaseModel):
    username: str
    password: str 