from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.schemas import UserLogin
from app.db.session import get_session

router = APIRouter(prefix='/auth' , tags=['auth'])


class TokenResponse(BaseModel):
    pass

@router.post('/token' , response_model=TokenResponse , status_code=status.HTTP_200_OK)
async def login(payload:UserLogin , session:AsyncSession=Depends(get_session)):
    pass
    