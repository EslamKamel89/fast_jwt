import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(... , min_length=2 , max_length=120 , description="Full name (2-120 chars)")
    email:EmailStr = Field(..., description="Valid email address")
    password:str = Field(...  , min_length=8, max_length=128, description="Password (min 8 chars)")
    
    @field_validator('name')
    @classmethod
    def normalize_name(cls , v:str)->str :
        if not isinstance(v,str): # type: ignore
            raise TypeError('name must be a string')
        return " ".join(v.strip().split())
    
    @field_validator('email')
    @classmethod
    def normalize_email(cls , v:str)->str :
        return v.lower().strip()
    
    @field_validator('password')
    @classmethod
    def check_password_complexity(cls , v:str)->str :
        if not isinstance(v,str): # type: ignore
            raise TypeError('password must of type string')
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError('password must contain at least one letter and one digit')
        return v
    
class UserRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int 
    name:str
    email:str
    role:str
    created_at:datetime|None = None
    
class UserLogin(BaseModel):
    username:str = Field(... , min_length=3 , max_length=120)
    password:str = Field(... , min_length=8 , max_length=128)