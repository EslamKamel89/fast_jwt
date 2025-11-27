from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.sandbox.models import Category, Product
from app.db.session import get_session

router = APIRouter(prefix='/sandbox/lesson1' , tags=['sandbox'])

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

@router.get('/lesson2/ex1')
async def sandbox8(session:AsyncSession=Depends(get_session)):
    stmt1 = (
        select(Product).where(Product.name=='Smart Watch')
    ) 
    stmt2 = (
        select(Product).filter_by(name='Smart Watch')
    )
    res = await session.execute(stmt2)
    products = res.scalars().all()
    return products

@router.get('/lesson2/ex2')
async def sandbox9(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product)
        .where(Product.price > 20)
        .where(Product.price < 50)
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lesson2/ex3')
async def sandbox10(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product)
        .where(Product.price > 20 , Product.price < 50)
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products


@router.get('/lesson2/ex4')
async def sandbox11(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product)
        .where(and_(Product.price > 20 , Product.price < 50))
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lesson2/ex5')
async def sandbox12(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product)
        .where(or_(Product.name.ilike("%laptop%") , Product.name.ilike('%galaxy%')))
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lesson2/ex6')
async def sandbox13(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product).where(Product.name.ilike('%LAP%'))
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lesson2/ex7')
async def sandbox14(session:AsyncSession=Depends(get_session)):
    stmt = (
        select(Product).order_by(Product.name.desc() , Product.price.desc())
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lesson2/ex8')
async def sandbox15(
    session:AsyncSession=Depends(get_session) , 
    page:Annotated[int , Query(min=1)] = 1 , 
    limit:Annotated[int , Query(min=1 , max=100)] = 10):
    offset = (page -1) * limit
    stmt = (
        select(Product).offset(offset).limit(limit)
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lessons2/ex9')
async def sandbox16(
    session:AsyncSession = Depends(get_session) , 
    min_price:Annotated[float|None , Query(min=1 , max = 99999999)] = None,
    max_price:Annotated[float|None , Query(min=1 , max = 99999999)] = None,
):
    stmt = select(Product)
    if min_price is not None : 
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None: 
        stmt = stmt.where(Product.price <= max_price)
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lessons2/ex10')
async def sandbox17(
    session:AsyncSession = Depends(get_session) , 
    q:Annotated[str|None , Query()] = None,
):
    stmt = select(Product)
    if q is not None : 
        stmt = stmt.where(Product.name.ilike(f'%{q}%'))
    res = await session.execute(stmt)
    products = res.scalars().all()
    return products

@router.get('/lessons2/ex11')
async def sandbox18(
    session:AsyncSession = Depends(get_session) , 
    page:Annotated[int , Query(min=1)]=1 , 
    limit:Annotated[int , Query(min=1,max=100)]=10
):
    offset = (page-1) * limit
    stmt = (
        select(Product).offset(offset).limit(limit)
    )
    res = await session.execute(stmt)
    products = res.scalars().all()
    return {
        "page":page , 
        "limit": limit , 
        "length" : len(products) ,
        "data": products,
    }

