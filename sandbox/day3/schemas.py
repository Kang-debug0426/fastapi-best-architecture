from pydantic import BaseModel,Field
#添加一个自定义验证器field_validator，验证字符串是不是有空格
from  pydantic import field_validator,EmailStr

class UserCreate(BaseModel):
    username:str=Field(...,min_length=3,max_length=50)
    age:int=Field(...,gt=0,lt=150)
    email:EmailStr

    @field_validator('username')
    @classmethod
    def username_no_space(cls,v):
        if ' ' in v:
            raise ValueError("username 不能包含空格")
        return v
class UserResponse(BaseModel):
    id:int
    username:str