from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Product

router = APIRouter()

@router.get("/summary")  # chỉ để /summary
def dashboard_summary(db: Session = Depends(get_db)):
    total_products = db.query(Product).count()

    # Tổng giá trị kho hiện tại = sum(stock * import_price)
    total_stock_value = db.query(
        func.sum(Product.stock * Product.import_price)
    ).scalar() or 0

    # Sản phẩm dưới min_stock
    low_stock = db.query(Product).filter(Product.stock < Product.min_stock).count()

    return {
        "total_products": total_products,
        "total_stock_value": float(total_stock_value),
        "low_stock": low_stock
    }
