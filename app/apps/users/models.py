from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING :
    from app.apps.sandbox.models import Order, Profile
    
class User(Base , TimestampMixin):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    email:Mapped[str] = mapped_column(String(200) , index=True , nullable=False , unique=True)
    name:Mapped[str] = mapped_column(String(100) , index=True , nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255) , nullable=False)
    role:Mapped[str] = mapped_column(String(50) , server_default=text("'user'") , index=True )
    orders:Mapped[list["Order"]] = relationship("Order"  , back_populates='user' , cascade='all, delete-orphan')
    profile:Mapped["Profile"] = relationship("Profile" , back_populates='user' , uselist=False)
    
