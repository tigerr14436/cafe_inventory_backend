from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models import (
    InventoryCheckSession,
    InventoryCheckDetail,
    Product
)

router = APIRouter(prefix="/inventory_check", tags=["Inventory Check"])


# ======================================================
# LẤY DỮ LIỆU KIỂM KHO THEO NGÀY
# ======================================================
@router.get("/{check_date}")
def get_inventory_by_date(check_date: date, db: Session = Depends(get_db)):
    session = (
        db.query(InventoryCheckSession)
        .filter(InventoryCheckSession.check_date == check_date)
        .first()
    )

    if session:
        # Nếu ngày đã kiểm kho → trả dữ liệu đã lưu, kèm unit, category, min_stock
        return {
            "check_date": session.check_date,
            "note": session.note,
            "items": [
                {
                    "product_id": d.product_id,
                    "product_name": d.product.name,
                    "unit": d.product.unit,
                    "category": d.product.category,
                    "min_stock": d.product.min_stock,
                    "system_stock": d.system_stock,
                    "real_stock": d.real_stock,
                    "difference": d.difference,
                    "note": d.note
                }
                for d in session.details
            ]
        }

    # Nếu ngày chưa kiểm kho → trả tồn hệ thống, kèm unit, category, min_stock
    products = db.query(Product).all()

    items = [
        {
            "product_id": p.id,
            "product_name": p.name,
            "unit": p.unit,
            "category": p.category,
            "min_stock": p.min_stock,
            "system_stock": p.stock,
            "real_stock": p.stock,
            "difference": 0,
            "note": ""
        }
        for p in products
    ]

    return {
        "check_date": check_date,
        "note": "",
        "items": items
    }


# ======================================================
# LƯU PHIÊN KIỂM KHO
# ======================================================
@router.post("/save")
def save_inventory_check(payload: dict, db: Session = Depends(get_db)):
    check_date = payload.get("check_date")
    note = payload.get("note", "")
    items = payload.get("items", [])

    if not check_date:
        raise HTTPException(status_code=400, detail="Missing check_date")

    # Kiểm tra phiên kiểm kho cũ
    old_session = (
        db.query(InventoryCheckSession)
        .filter(InventoryCheckSession.check_date == check_date)
        .first()
    )

    # Nếu có → xóa để thay thế
    if old_session:
        db.delete(old_session)
        db.commit()

    # Tạo phiên mới
    new_session = InventoryCheckSession(
        check_date=check_date,
        note=note
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Lưu chi tiết kiểm kho
    for item in items:
        detail = InventoryCheckDetail(
            session_id=new_session.id,
            product_id=item["product_id"],
            system_stock=item["system_stock"],
            real_stock=item["real_stock"],
            difference=item["difference"],
            note=item.get("note", "")
        )
        db.add(detail)

        # Cập nhật tồn kho thực tế vào bảng Product
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if product:
            product.stock = item["real_stock"]

    db.commit()

    return {"message": "Đã lưu dữ liệu kiểm kho thành công!"}
