from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.database import get_db
from app import models

router = APIRouter()

# ======================================================
# KPI TỔNG QUAN
# ======================================================
@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):

    total_products = db.query(models.Product).count()

    total_stock_quantity = (
        db.query(func.sum(models.Product.stock)).scalar()
    ) or 0

    total_stock_value = (
        db.query(
            func.sum(models.Product.stock * models.Product.import_price)
        ).scalar()
    ) or 0

    low_stock = (
        db.query(models.Product)
        .filter(models.Product.stock < models.Product.min_stock)
        .count()
    )

    return {
        "total_products": total_products,
        "total_stock_quantity": int(total_stock_quantity),
        "total_stock_value": float(total_stock_value),
        "low_stock": low_stock
    }


# ======================================================
# BIỂU ĐỒ NHẬP – XUẤT 7 NGÀY
# ======================================================
@router.get("/stock-chart")
def stock_chart(db: Session = Depends(get_db)):

    DAYS = 7
    today = date.today()

    labels = []
    imports = []
    exports = []

    for i in range(DAYS):
        day = today - timedelta(days=DAYS - i - 1)
        labels.append(day.strftime("%d/%m"))

        import_qty = (
            db.query(func.sum(models.ImportDetail.quantity))
            .join(models.Import, models.ImportDetail.import_id == models.Import.id)
            .filter(models.Import.import_date == day)
            .scalar()
        ) or 0

        export_qty = (
            db.query(func.sum(models.ExportDetail.quantity))
            .join(models.Export, models.ExportDetail.export_id == models.Export.id)
            .filter(models.Export.export_date == day)
            .scalar()
        ) or 0

        imports.append(int(import_qty))
        exports.append(int(export_qty))

    current_inventory = (
        db.query(func.sum(models.Product.stock)).scalar()
    ) or 0

    return {
        "labels": labels,
        "imports": imports,
        "exports": exports,
        "current_inventory": int(current_inventory)
    }


# ======================================================
# DANH SÁCH SẢN PHẨM TỒN THẤP
# ======================================================
@router.get("/low-stock")
def low_stock_products(db: Session = Depends(get_db)):

    products = (
        db.query(models.Product)
        .filter(models.Product.stock < models.Product.min_stock)
        .all()
    )

    return [
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "stock": p.stock,
            "min_stock": p.min_stock,
            "unit": p.unit
        }
        for p in products
    ]


# ======================================================
# TOP 5 NHẬP NHIỀU NHẤT
# ======================================================
@router.get("/top-import-products")
def top_import_products(db: Session = Depends(get_db)):

    results = (
        db.query(
            models.Product.name.label("product_name"),
            func.sum(models.ImportDetail.quantity).label("quantity")
        )
        .join(
            models.ImportDetail,
            models.Product.id == models.ImportDetail.product_id
        )
        .group_by(models.Product.id)
        .order_by(func.sum(models.ImportDetail.quantity).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "product_name": r.product_name,
            "quantity": int(r.quantity)
        }
        for r in results
    ]


# ======================================================
# TOP 5 XUẤT NHIỀU NHẤT
# ======================================================
@router.get("/top-export-products")
def top_export_products(db: Session = Depends(get_db)):

    results = (
        db.query(
            models.Product.name.label("product_name"),
            func.sum(models.ExportDetail.quantity).label("quantity")
        )
        .join(
            models.ExportDetail,
            models.Product.id == models.ExportDetail.product_id
        )
        .group_by(models.Product.id)
        .order_by(func.sum(models.ExportDetail.quantity).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "product_name": r.product_name,
            "quantity": int(r.quantity)
        }
        for r in results
    ]