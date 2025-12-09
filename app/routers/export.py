from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app import models

router = APIRouter(tags=["Exports"])

# =========================
# TẠO PHIẾU XUẤT KHO
# =========================
@router.post("/")
def create_export(data: dict, db: Session = Depends(get_db)):

    if "code" not in data or "receiver" not in data or "export_date" not in data:
        raise HTTPException(400, "Thiếu dữ liệu phiếu xuất!")

    if "details" not in data or len(data["details"]) == 0:
        raise HTTPException(400, "Chi tiết sản phẩm không được để trống!")

    # map receiver → customer
    new_export = models.Export(
        code=data["code"],
        customer=data["receiver"],       # dùng cột customer trong DB
        export_date=date.fromisoformat(data["export_date"])
    )
    db.add(new_export)
    db.commit()
    db.refresh(new_export)

    for d in data["details"]:
        product = db.query(models.Product).filter(models.Product.id == d["product_id"]).first()
        if not product:
            raise HTTPException(404, "Sản phẩm không tồn tại!")
        if product.stock < d["quantity"]:
            raise HTTPException(400, f"Sản phẩm {product.name} không đủ tồn kho!")

        detail = models.ExportDetail(
            export_id=new_export.id,
            product_id=d["product_id"],
            quantity=d["quantity"],
            price=d["price"],
            total_price=d["quantity"] * d["price"]
        )
        db.add(detail)

        product.stock -= d["quantity"]

    db.commit()

    return {"message": "Xuất kho thành công!", "export_id": new_export.id}



# =========================
# DANH SÁCH PHIẾU XUẤT
# =========================
@router.get("/")
def list_exports(db: Session = Depends(get_db)):
    exports = db.query(models.Export).all()

    result = []
    for exp in exports:
        details = db.query(models.ExportDetail).filter(
            models.ExportDetail.export_id == exp.id
        ).all()

        total = sum(d.total_price for d in details)

        result.append({
            "id": exp.id,
            "code": exp.code,
            "receiver": exp.receiver,
            "export_date": exp.export_date,
            "total": total
        })

    return result


# =========================
# CHI TIẾT 1 PHIẾU XUẤT
# =========================
@router.get("/{export_id}")
def get_export_details(export_id: int, db: Session = Depends(get_db)):

    exp = db.query(models.Export).filter(models.Export.id == export_id).first()
    if not exp:
        raise HTTPException(404, "Không tìm thấy phiếu xuất!")

    details = (
        db.query(models.ExportDetail, models.Product)
        .join(models.Product, models.ExportDetail.product_id == models.Product.id)
        .filter(models.ExportDetail.export_id == export_id)
        .all()
    )

    return {
        "export": {
            "id": exp.id,
            "code": exp.code,
            "receiver": exp.receiver,
            "export_date": exp.export_date.isoformat()
        },
        "details": [
            {
                "product_id": p.id,
                "product_name": p.name,
                "unit": p.unit,
                "quantity": d.quantity,
                "price": d.price,
                "total_price": d.total_price
            }
            for d, p in details
        ]
    }
