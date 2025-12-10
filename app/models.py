from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Text
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
    import_price = Column(Numeric(10,2))
    sell_price = Column(Numeric(10,2))
    stock = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)
    description = Column(Text)

    # Quan hệ với phiếu nhập và xuất
    imports = relationship("ImportDetail", back_populates="product", cascade="all, delete-orphan")
    exports = relationship("ExportDetail", back_populates="product", cascade="all, delete-orphan")


# =========================
# BẢNG PHIẾU NHẬP KHO
# =========================
class Import(Base):
    __tablename__ = "imports"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)  # VD: PNK00124
    supplier = Column(String)
    import_date = Column(Date)

    details = relationship("ImportDetail", back_populates="import_parent", cascade="all, delete-orphan")


# =========================
# BẢNG CHI TIẾT NHẬP KHO
# =========================
class ImportDetail(Base):
    __tablename__ = "import_details"

    id = Column(Integer, primary_key=True, index=True)
    import_id = Column(Integer, ForeignKey("imports.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Numeric(10,2))
    total_price = Column(Numeric(10,2))

    import_parent = relationship("Import", back_populates="details")
    product = relationship("Product", back_populates="imports")


# =========================
# BẢNG PHIẾU XUẤT KHO
# =========================
class Export(Base):
    __tablename__ = "exports"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)
    customer = Column(String)
    export_date = Column(Date)

    details = relationship("ExportDetail", back_populates="export_parent", cascade="all, delete-orphan")


# =========================
# BẢNG CHI TIẾT XUẤT KHO
# =========================
class ExportDetail(Base):
    __tablename__ = "export_details"

    id = Column(Integer, primary_key=True, index=True)
    export_id = Column(Integer, ForeignKey("exports.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Numeric(10,2))
    total_price = Column(Numeric(10,2))

    export_parent = relationship("Export", back_populates="details")
    product = relationship("Product", back_populates="exports")

# =========================
# BẢNG PHIÊN KIỂM KHO
# =========================
class InventoryCheckSession(Base):
    __tablename__ = "inventory_check_sessions"

    id = Column(Integer, primary_key=True, index=True)
    check_date = Column(Date, nullable=False)
    note = Column(String)  # ghi chú chung cho cả phiên (nếu cần)

    details = relationship("InventoryCheckDetail", back_populates="session", cascade="all, delete-orphan")

# =========================
# BẢNG CHI TIẾT KIỂM KHO
# =========================
class InventoryCheckDetail(Base):
    __tablename__ = "inventory_check_details"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("inventory_check_sessions.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    system_stock = Column(Integer, nullable=False)
    real_stock = Column(Integer, nullable=False)
    difference = Column(Integer, nullable=False)
    note = Column(String)

    session = relationship("InventoryCheckSession", back_populates="details")
    product = relationship("Product")