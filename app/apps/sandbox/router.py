from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter(prefix='/sandbox' , tags=['sandbox'])

@router.get('')
async def sandbox(session:AsyncSession=Depends(get_session)):
    return {"data":{
        "message":"it works"
    }}