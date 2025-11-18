from sqlalchemy import Boolean, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class RefreshToken(Base ,TimestampMixin):
    __tablename__ = 'refresh_tokens'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id' , ondelete='CASCADE') ,nullable=True )
    token:Mapped[str] = mapped_column(String(512) , nullable=False , index=True)
    revoked:Mapped[bool] = mapped_column(Boolean , nullable=False , server_default=text("0"))