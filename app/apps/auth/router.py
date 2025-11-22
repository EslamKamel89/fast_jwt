from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.auth.models import RefreshToken
from app.apps.auth.repository import RefreshTokenRepository
from app.apps.auth.validation import RefreshAccessTokenResponse, TokenResponse
from app.apps.users.repository import UserRepository
from app.apps.users.schemas import UserLogin
from app.core.security import Security
from app.db.session import get_session

router = APIRouter(prefix='/auth' , tags=['auth'])


@router.post('/token' , response_model=TokenResponse , status_code=status.HTTP_200_OK)
async def login(payload:UserLogin , session:AsyncSession=Depends(get_session)):
    repo = UserRepository(session)
    user = await repo.get_by_email(payload.email)
    if not user or not Security.verify_password(payload.password , user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , detail='Invalid credentials')
    access = Security.create_access_token(str(user.id) , extra={'role':user.role})
    refresh = Security.create_refresh_token(str(user.id))
    rt_repo = RefreshTokenRepository(session)
    await rt_repo.create_token(user.id , refresh)
    return TokenResponse(access_token=access , refresh_token=refresh  , token_type='bearer')
    
    
@router.post('/refresh' , response_model=TokenResponse)
async def refresh(refresh_token:str = Body(..., embed=True) , session:AsyncSession=Depends(get_session)):
    try:
        payload = Security.decode_token(refresh_token)
    except Exception as e:
        raise e
    user_id:Any = payload.get('sub')
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , detail="Invalid token")
    rt_repo = RefreshTokenRepository(session)
    existing = await rt_repo.get_by_token(refresh_token)
    if existing is None  or existing.revoked: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , detail="Refresh token is invalid or revoked")
    await rt_repo.revoke(existing.id)
    new_access = Security.create_access_token(str(user_id))
    new_refresh = Security.create_refresh_token(str(user_id))
    await rt_repo.create_token(int(user_id) , new_refresh)
    return TokenResponse(access_token=new_access , token_type='bearer' , refresh_token=new_refresh)

@router.post('/logout' , status_code=status.HTTP_204_NO_CONTENT)
async def logout(refresh_token:str = Body(...,embed=True) , session:AsyncSession=Depends(get_session)):
    rt_repo = RefreshTokenRepository(session)
    rec = await rt_repo.get_by_token(refresh_token)
    if rec is None : 
        return None 
    await rt_repo.revoke(rec.id)
    return None