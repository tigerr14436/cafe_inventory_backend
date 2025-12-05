from sqlalchemy import Column, Integer, String, Numeric, Text
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), index=True)
    name = Column(String, index=True)
    category = Column(String(100))
    unit = Column(String)

    import_price = Column(Numeric(12, 2), default=0)
    sell_price = Column(Numeric(12, 2), default=0)

    stock = Column(Numeric(12, 3), default=0)
    min_stock = Column(Integer, default=0)

    description = Column(Text)
    image_url = Column(Text)
