import uuid,redis

from fastapi import HTTPException, Header
from jose import JWTError, jwt#导入JWTError和jwt模块，用于处理JWT相关的错误和操作
from datetime import datetime, timedelta#导入datetime和timedelta模块，用于处理日期
import bcrypt
from fastapi import APIRouter
from schemas import LoginRequest
r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True, password="cjk123")
router =APIRouter()

SECRET_KEY="cjk_secret_key_123456"#这是一个密钥，用于加密和解密JWT。这个密钥应该是一个随机的字符串，长度至少应该是32个字符。这个密钥应该保存在安全的地方，不要泄露给任何人。
ALGORITHM="HS256"#这是一个算法，用于加密和解密JWT。这个

def hash_password(password: str) -> str:#
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#这是一个函数，用于加密密码。它接受一个字符串类型的密码作为输入，返回一个字符串类型的哈希值作为输出
# 。它使用bcrypt算法来加密密码，并且生成一个随机的盐值来增强安全性。最后，它把哈希值转换成字符串类型并返回。


def verify_password(password: str, hashed: str) -> bool:
#这是一个函数，用于验证密码。它接受一个字符串类型的密码和一个字符串类型的哈希值作为输入，
# 返回一个布尔值作为输出。它使用bcrypt算法来验证密码是否与哈希值匹配。如果匹配，返回True；否则，返回False。
    return bcrypt.checkpw(password.encode(), hashed.encode())

fake_user={
        "luchia": {
        "username": "luchia",
        "hashed_password": hash_password("123456")
    }
}



def verify_token(authorization:str=Header(...)):#这里的Header(...)表示这个参数是必须的，如
    #果请求头中没有这个参数，FastAPI会自动返回一个400错误
    try:
        token=authorization.split("Bearer ")[1]#这是把请求头中的Authorization字段的值按照"Bearer "这个字符串进行分割，
        #得到一个列表，然后取这个列表的第二个元素（索引为1），也就是JWT令牌的部分。因为Authorization字段的值通常是以"Bearer "开头，
        # #后面跟着JWT令牌，所以我们需要把"Bearer "这个前缀去掉，才能得到纯粹的JWT令牌。
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])#这是使用jwt模块的decode函数来解码JWT令牌。它接受三个参数：token是要解码的JWT令牌，
        #SECRET_KEY是用于解密JWT的密钥，algorithms是一个列表，指定了允许使用的加密算法。
        #在这个例子中，我们只允许使用HS256算法来解密JWT。
        username=payload.get("sub")#这是从解码后的JWT的payload中获取用户名。用户名是用户登录时指定的用户名，用于标识用户。
        session_id=payload.get("session_id")#这是从解码后的JWT的payload中获取session_id字段的值。这个值是在用户登录时生成的一个唯一的会话ID，用于标识用户的登录状态。
        if not  r.exists(f"ainotes:token:{username}:{session_id}"):
              raise HTTPException(status_code=401, detail="token 已过期")
        return username
    except:    
        raise HTTPException (status_code=401, detail="无效 token")    
    
    
@router.post("/auth/login")
def login(data : LoginRequest):
    user=fake_user.get(data.username)#这是从fake_user这个字典中获取用户信息。fake_user是一个模拟的用户数据库，
    #key是用户名，value是一个包含用户名和哈希密码的字典。当我们调用login函数时，
    # 会根据输入的用户名从fake_user中获取对应的用户信息。如果用户不存在，就会返回None。
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="密码错误")
    session_id=str(uuid.uuid4())#这是生成一个唯一的会话ID。uuid.uuid4()函数会生成一个随机的UUID对象，
    #然后我们把它转换成字符串类型。这个会话ID可以用来标识用户的登录状态，或者存储一些与用户相关的信息。
    payload = {
        "sub": data.username,
        "session_id": session_id,
        "exp": datetime.utcnow() + timedelta(hours=1)#这是设置JWT令牌的过期时间为1小时。
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)#这是使用jwt模块的encode函数来生成JWT令牌。
     #它接受三个参数：payload是要编码的JWT的载荷，

    #往 redis中存session，key格式和fba一样
    r.set(f"ainotes:token:{data.username}:{session_id}", "1", ex=3600)#这是把会话ID和1这个字符串存储到redis中，过期时间为3600秒。#key的格式是
  #"ainotes:token:{session_id}"，value是"1"，ex参数表示这个键值对的过期时间是秒。把会话ID和一个简单的字符串"1"存储到redis中，以表示用户的登录状态，并且设置这个键值对在1小时后过期。
    return {"access_token": token, "token_type": "bearer"}


@router.delete("/auth/logout"  )
def logout(authorization:str=Header(...)):#这是一个接口函数，用于处理用户的登出请求。它接受一个参数authorization，这个参数是从请求头中获取的，必须包含在请求头中。
    try:
        token=authorization.split("Bearer ")[1]#这是把请求头中的Authorization字段的值按照"Bearer "这个字符串进行分割，
        #得到一个列表，然后取这个列表的第二个元素（索引为1），也就是JWT令牌的部分。因为Authorization字段的值通常是以"Bearer "开头，
        #后面跟着JWT令牌，所以我们需要把"Bearer "这个前缀去掉，才能得到纯粹的JWT令牌。
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])#这是使用jwt模块的decode函数来解码JWT令牌。它接受三个参数：token是要解码的JWT令牌，
        #SECRET_KEY是用于解密JWT的密钥，algorithms是一个列表，指定了允许使用的加密算法。
        #在这个例子中，我们只允许使用HS256算法来解密JWT。
        session_id=payload.get("session_id")#这是从解码后的JWT的payload中获取session_id字段的值。这个值是在用户登录时生成的一个唯一的会话ID，用于标识用户的登录状态。
        username=payload.get("sub")#这是从解码后的JWT的payload中获取用户名。用户名是用户登录时指定的用户名，用于标识用户。
        r.delete(f"ainotes:token:{username}:{session_id}")#这是从redis中删除这个会话ID对应的键值对。这样做的目的是为了让这个会话失效，防止被再次使用。
        return {"details": "已退出登录"}
    except:
        raise HTTPException (status_code=401, detail="无效 token")
