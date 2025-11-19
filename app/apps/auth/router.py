from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.auth.validation import RefreshAccessTokenResponse, TokenResponse
from app.apps.users.models import RefreshToken
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
    refresh_model = RefreshToken(user_id=user.id , token=refresh)
    session.add(refresh_model)
    await session.commit()
    return TokenResponse(access_token=access , refresh_token=refresh  , token_type='bearer')
    
    
@router.post('/refresh')
async def refresh(refresh_token:str , session:AsyncSession=Depends(get_session)):
    try:
        payload = Security.decode_token(refresh_token)
    except Exception as e:
        raise e
    q = select(RefreshToken).where(RefreshToken.token == refresh_token , RefreshToken.revoked == False)
    res = await session.execute(q)
    row = res.scalar_one_or_none()
    if row is None : 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED , detail="Invalid token")
    user_id:Any = payload.get('sub')
    access = Security.create_access_token(user_id)
    return RefreshAccessTokenResponse(access_token=access , token_type='bearer')

    