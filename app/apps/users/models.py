from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class User(Base , TimestampMixin):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    email:Mapped[str] = mapped_column(String(200) , index=True , nullable=False , unique=True)
    name:Mapped[str] = mapped_column(String(100) , index=True , nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255) , nullable=False)
    role:Mapped[str] = mapped_column(String(50) , server_default='user' , index=True )
    