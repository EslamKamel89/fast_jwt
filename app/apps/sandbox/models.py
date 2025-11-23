from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

product_category = Table(
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
    categories:Mapped[list["Category"]] = relationship('Category' , secondary='product_categories' , back_populates='categories')

class Category(Base,TimestampMixin) :
    id:Mapped[int]  = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(String(100) , unique=True , nullable=False , index=True)
    categories:Mapped[list[Product]] = relationship(Product , secondary='product_categories' , back_populates='products')