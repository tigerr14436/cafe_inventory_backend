from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app import models

router = APIRouter(tags=["Imports"]) 

# =========================
# TẠO PHIẾU NHẬP
# =========================
@router.post("/")
def create_import(data: dict, db: Session = Depends(get_db)):

    if "code" not in data or "supplier" not in data or "import_date" not in data:
        raise HTTPException(400, "Thiếu dữ liệu phiếu nhập!")

    if "details" not in data or len(data["details"]) == 0:
        raise HTTPException(400, "Chi tiết sản phẩm không được để trống!")

    # Tạo phiếu nhập
    new_import = models.Import(
        code=data["code"],
        supplier=data["supplier"],
        import_date=date.fromisoformat(data["import_date"])
    )
    db.add(new_import)
    db.commit()
    db.refresh(new_import)

    # Tạo chi tiết phiếu nhập
    for d in data["details"]:
        detail = models.ImportDetail(
            import_id=new_import.id,
            product_id=d["product_id"],
            quantity=d["quantity"],
            price=d["price"],
            total_price=d["quantity"] * d["price"]
        )
        db.add(detail)

        # Cập nhật stock sản phẩm
        product = db.query(models.Product).filter(models.Product.id == d["product_id"]).first()
        if product:
            product.stock += d["quantity"]

    db.commit()

    return {"message": "Nhập kho thành công!", "import_id": new_import.id}
# =========================
# LẤY DANH SÁCH PHIẾU NHẬP
# =========================
@router.get("/")
def get_imports(db: Session = Depends(get_db)):
    imports = db.query(models.Import).all()

    result = []
    for imp in imports:
        # Lấy tất cả detail theo import_id
        details = db.query(models.ImportDetail).filter(
            models.ImportDetail.import_id == imp.id
        ).all()

        total_price = sum(d.total_price for d in details)

        result.append({
            "id": imp.id,
            "code": imp.code,
            "supplier": imp.supplier,
            "import_date": imp.import_date,
            "total": total_price
        })

    return result
# =========================
# LẤY CHI TIẾT 1 PHIẾU NHẬP
# =========================
@router.get("/{import_id}")
def get_import_details(import_id: int, db: Session = Depends(get_db)):

    imp = db.query(models.Import).filter(models.Import.id == import_id).first()
    if not imp:
        raise HTTPException(404, "Không tìm thấy phiếu nhập!")

    details = (
        db.query(models.ImportDetail, models.Product)
        .join(models.Product, models.ImportDetail.product_id == models.Product.id)
        .filter(models.ImportDetail.import_id == import_id)
        .all()
    )

    return {
        "import": {
            "id": imp.id,
            "code": imp.code,
            "supplier": imp.supplier,
            "import_date": imp.import_date.isoformat()
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