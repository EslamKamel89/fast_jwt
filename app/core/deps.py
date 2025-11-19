from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.core.security import Security

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/token')
class CurrentUser(BaseModel) :
    user_id:int
    role:str
async def get_current_user(token:str=Depends(oauth2_schema))->CurrentUser :
    try:
        payload = Security.decode_token(token)
        sub = payload.get('sub')
        role = payload.get('role' , 'user')
        if sub is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Invalid Token')
        return CurrentUser(user_id=int(sub) , role=role)
    except Exception :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail= "Invalid token")
    
async def admin_required(user:CurrentUser=Depends(get_current_user)):
    if user.role != 'admin' : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Admin only")
    return user
    
