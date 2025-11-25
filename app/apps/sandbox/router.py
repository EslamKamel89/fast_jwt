from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.sandbox.models import Category
from app.db.session import get_session

router = APIRouter(prefix='/sandbox' , tags=['sandbox'])

@router.get('/lesson1/categories')
async def sandbox(session:AsyncSession=Depends(get_session)): 
    stmt = select(Category).order_by(Category.name)
    res = await session.execute(stmt)
    categories:Sequence[Category] = res.scalars().all()
    return {"data":{"categories":categories }} 