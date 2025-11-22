from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.auth.models import RefreshToken


class RefreshTokenRepository():
    def __init__(self , session:AsyncSession):
        self.session = session
        
    async def create_token(self , user_id:int  , token:str)->RefreshToken:
        pass
    
    async def get_by_token(self , token:str)->Optional[RefreshToken]:
        pass
    
    async def revoke(self , token_id:int)->None:
        pass
    
    async def revoke_all_for_user(self , user_id:int)->None:
        pass