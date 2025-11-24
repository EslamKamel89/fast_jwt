from __future__ import annotations

import asyncio
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.sandbox.models import (Category, Order, OrderItem, Product,
                                     Profile)
from app.apps.users.models import User
from app.core.security import Security
from app.db.session import AsyncSessionLocal  # your async_sessionmaker

# from decimal import Decimal
# from typing import List



USERS = [
    {"name": "Alice", "email": "alice@example.com", "password": "password", "role": "user"},
    {"name": "Bob", "email": "bob@example.com", "password": "password", "role": "user"},
    {"name": "Carol", "email": "carol@example.com", "password": "password", "role": "admin"},
]

PRODUCTS:list[dict[str, str|float]] = [
    {"name": "Smart Watch", "price": 199.99},
    {"name": "Bluetooth Headphones", "price": 129.50},
    {"name": "Wireless Charger", "price": 29.99},
]
CATEGORIES = ["Electronics", "Accessories", "Gadgets"]

async def create_users(session:AsyncSession)->list[User]:
    created:list[User] = []
    for u in USERS:
        existing = (await session.execute(
            select(User).where(User.email == u['email'])
        )).scalar_one_or_none()
        if existing is not None:
            created.append(existing)
            continue
        user = User(
            name=u['name'] ,
            email=u['email'] ,
            password_hash=Security.hash_password(u['password']) ,
            role=u['role'] ,
        )
        session.add(user)
        await session.flush()
        profile = Profile(
            user_id=user.id ,
            bio=f"Hello, I'm {u['name']}",
            avatar_url=None
        )
        session.add(profile)
        await session.flush()
        created.append(user)
    return created

async def create_categories(session:AsyncSession)->list[Category]:
    created:list[Category] = []
    for name in CATEGORIES :
        existing = (await session.execute(
            select(Category).where(Category.name == name)
        )).scalar_one_or_none()
        if existing is not None:
            created.append(existing)
            continue
        cat = Category(name=name)
        session.add(cat)
        await session.flush()
        created.append(cat)
    return created

async def create_products_and_link(session:AsyncSession , categories:list[Category])->list[Product]:
    created:list[Product] = []
    for  i,p in enumerate(PRODUCTS):
        existing = (await session.execute(
            select(Product).where(Product.name == p['name'])
        )).scalar_one_or_none()
        if existing is not None : 
            created.append(existing)
            continue
        prod = Product(name=p["name"], price=p["price"])
        prod.categories.append(categories[0])
        if i % 2 == 0 : 
            prod.categories.append(categories[1])
        else :
            prod.categories.append(categories[2])
        session.add(prod)
        await session.flush()
        created.append(prod)
    return created

async def create_orders(session:AsyncSession  , users:list[User] , products:list[Product])->list[Order]:
    created:list[Order] = []
    for u in users:
        if u.role == 'admin':
            continue
        order = Order(user_id = u.id)
        session.add(order)
        await session.flush()
        prods = random.sample(products ,2)
        for prod in prods:
            oi = OrderItem(order_id=order.id , product_id=prod.id , quantity=1 , unit_price=prod.price)
            session.add(oi)
    return created
 
async def run_seed():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            print(".............................................")
            print("........Creating users + profiles............")
            users = await create_users(session)
            print(f"......Created/loaded {len(users)} users......")
            print(".............................................")
            
            print(".............................................")
            print(".............Creating categories.............")
            categories = await create_categories(session)
            print(f"Created/loaded {len(categories)} categories")
            print(".............................................")
            
            print(".............................................")
            print("..Creating products and linking categories..")
            products = await create_products_and_link(session, categories)
            print(f"...Created/loaded {len(products)} products...")
            print(".............................................")
            
            print(".............................................")
            print("..........Creating orders for users..........")
            await create_orders(session, users, products)
            print("...............Orders created...............")
            print(".............................................")
            
if __name__ == '__main__':
    asyncio.run(run_seed())