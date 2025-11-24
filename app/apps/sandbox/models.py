from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.apps.users.models import User

product_categories = Table(
    'product_categories' , 
    Base.metadata , 
    Column('product_id' , Integer , ForeignKey('products.id' , ondelete='CASCADE') , primary_key=True),
    Column('category_id' , Integer , ForeignKey('categories.id' , ondelete='CASCADE') , primary_key=True),
)

class Product(Base , TimestampMixin):
    __tablename__='products'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(String(100) , index=True , nullable=False , unique=True)
    price:Mapped[float] = mapped_column(Float, nullable=False , default=0.0)
    categories:Mapped[list["Category"]] = relationship('Category' , secondary=product_categories , back_populates='products')

class Category(Base,TimestampMixin) :
    __tablename__='categories'
    id:Mapped[int]  = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(String(100) , unique=True , nullable=False , index=True)
    products:Mapped[list["Product"]] = relationship("Product" , secondary=product_categories , back_populates='categories')
    
class Order(Base , TimestampMixin):
    __tablename__='orders'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer , ForeignKey('users.id' , ondelete='SET NULL') , nullable=True)
    user :Mapped["User"] = relationship("User" , back_populates='orders' )
    items: Mapped[list['OrderItem']] = relationship('OrderItem' , back_populates='order' , cascade="all, delete-orphan")
    
class OrderItem(Base ,TimestampMixin):
    __tablename__='order_items'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    order_id:Mapped[int] = mapped_column(Integer , ForeignKey('orders.id' , ondelete='CASCADE'), nullable=False)
    product_id:Mapped[int] = mapped_column(Integer , ForeignKey('products.id' , ondelete='SET NULL'))
    quantity:Mapped[int] = mapped_column(Integer , nullable=False, default=1)
    unit_price:Mapped[float] = mapped_column(Float , nullable=False , default=0.0)
    order:Mapped["Order"] = relationship("Order" , back_populates='items')
    product:Mapped["Product"] = relationship("Product")
    
class Profile(Base , TimestampMixin):
    __tablename__='profiles' 
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer , ForeignKey('users.id' , ondelete='CASCADE') , unique=True , nullable=False )
    bio:Mapped[str] = mapped_column(String(500) , nullable=True)
    avatar_url:Mapped[str] = mapped_column(String(255) , nullable=True)
    user:Mapped["User"] = relationship("User" , back_populates='profile'  , uselist=False)