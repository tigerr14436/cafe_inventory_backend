from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


# =========================
# BẢNG SẢN PHẨM
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)

    category = Column(String)
    unit = Column(String)
    import_price = Column(Float)
    sell_price = Column(Float)

    stock = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)

    description = Column(String)

    # Quan hệ: 1 sản phẩm -> nhiều chi tiết nhập kho
    imports = relationship("ImportDetail", back_populates="product")


# =========================
# BẢNG PHIẾU NHẬP KHO
# =========================
class Import(Base):
    __tablename__ = "imports"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)          # VD: PNK00124
    supplier = Column(String)                  # Nhà cung cấp
    import_date = Column(Date)                 # Ngày nhập

    # Quan hệ: 1 phiếu nhập -> nhiều sản phẩm
    details = relationship("ImportDetail", back_populates="import_parent")


# =========================
# BẢNG CHI TIẾT NHẬP KHO
# =========================
class ImportDetail(Base):
    __tablename__ = "import_details"

    id = Column(Integer, primary_key=True, index=True)

    import_id = Column(Integer, ForeignKey("imports.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer)
    price = Column(Float)       # đơn giá nhập
    total_price = Column(Float)

    # quan hệ 2 chiều
    import_parent = relationship("Import", back_populates="details")
    product = relationship("Product", back_populates="imports")