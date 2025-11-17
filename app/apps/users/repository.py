from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.models import User
from app.core.security import Security


class UserRepository:
    def __init__(self , session:AsyncSession):
        self.session = session
    
    async def create(self , name:str , email:str , password:str , role:str='user')->User:
        user = User(
            name=name , 
            email=email.lower().strip() , 
            password=Security.hash_password(password) ,
            role=role ,
            )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        await self.session.commit()
        return user
    
    async def get_by_email(self, email:str)->Optional[User]:
        stmt = select(User).filter(User.email == email)
        res = await self.session.execute(stmt)
        user: User|None = res.scalar_one_or_none()
        return user