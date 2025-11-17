from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.repository import UserRepository
from app.apps.users.schemas import UserCreate, UserRead
from app.db.session import get_session

router = APIRouter(prefix='/users' , tags=['users'])

@router.post('/' , response_model=UserRead , status_code=status.HTTP_201_CREATED)
async def register(payload:UserCreate , session:AsyncSession=Depends(get_session)):
    repo = UserRepository(session)
    existing = await repo.get_by_email(payload.email)
    if existing :
        raise HTTPException(status.HTTP_409_CONFLICT , detail='User exist')
    user = await repo.create(name=payload.name , email=payload.email , password=payload.password)
    return user
