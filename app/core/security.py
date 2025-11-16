from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'] , depreciated='auto')
def has_password(password:str)->str :
    return pwd_context.hash(password)
def verify_password(plain:str , hashed:str)->bool :
    return pwd_context.verify(plain , hashed)

def create_access_token(subject:str, extra: Dict[str , Any]|None = None) -> str : 
    payload:Dict[str, Any] = {'sub':subject}
    if extra : 
        payload.update(extra)
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES)
    payload['expire'] = expire
    return jwt.encode(claims=payload , key=settings.JWT_SECRET , algorithm=settings.JWT_ALG)
        
