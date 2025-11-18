from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.auth.validation import TokenResponse
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
    return TokenResponse(access_token=access , refresh_token=refresh  , token_type='Bearer')
    
    
    