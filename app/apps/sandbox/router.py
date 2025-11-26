from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.sandbox.models import Category, Product
from app.db.session import get_session

router = APIRouter(prefix='/sandbox' , tags=['sandbox'])

@router.get('/lesson1/ex1')
async def sandbox(session:AsyncSession=Depends(get_session)): 
    stmt = select(Category).order_by(Category.name.desc()).where(Category.name.ilike('%electronics%'))
    res = await session.execute(stmt)
    categories:Sequence[Category] = res.scalars().all()
    return {"data":{"categories":categories }} 

@router.get('/lesson1/ex2')
async def sandbox2(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Category)
        .where(Category.id > 2)
        .where(Category.name != 'Clothes')
        )
    res = await session.execute(stmt)
    categories:Sequence[Category] = res.scalars().all()
    return categories

@router.get('/lesson1/ex3')
async def sandbox3(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Category)
        .where(or_(
            Category.name.ilike('%Electronics%') , 
            Category.name.ilike('%kitchen%')
        ))
    )
    res  = await session.execute(stmt)
    categories:Sequence[Category] = res.scalars().all()
    return categories

@router.get('lesson1/ex4')
async def sandbox4(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product)
        .order_by(Product.price.desc())
        .limit(10)
        .offset(10)
    )
    res = await session.execute(stmt)
    categories:Sequence[Product] = res.scalars().all()
    return categories

@router.get('lesson1/ex5')
async def sandbox5(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product)
        .where(Product.price > 100)
        .where(Product.price < 200)
    )
    res = await session.execute(stmt)
    products:Sequence[Product] = res.scalars().all()
    return products

@router.get('/lesson1/ex6')
async def sandbox6(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Category)
        .where(Category.id == 1)
    )
    res = await session.execute(stmt)
    # category:Category|None = res.scalars().first()
    # category:Category|None = res.scalar_one_or_none()
    category:Category = res.scalar_one()
    return category

@router.get('/lesson1/ex7')
async def sandbox7(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(func.count(Product.id))
    )
    res = await session.execute(stmt)
    count = res.scalar_one()
    return {'count':count}