from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    name = Column(String, index=True)
    category = Column(String)
    unit = Column(String)
    import_price = Column(Float)
    sell_price = Column(Float)
    stock = Column(Integer)
    min_stock = Column(Integer)
    description = Column(String)
