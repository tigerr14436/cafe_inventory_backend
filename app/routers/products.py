from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(tags=["Products"])

# GET ALL
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

# GET BY ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product

# CREATE
@router.post("/products")
def create_product(data: dict, db: Session = Depends(get_db)):

    # Kiểm tra SKU trùng
    exist_sku = db.query(models.Product).filter(models.Product.sku == data["sku"]).first()
    if exist_sku:
        raise HTTPException(status_code=400, detail="Sản phẩm với SKU này đã tồn tại!")

    # Kiểm tra TÊN trùng
    exist_name = db.query(models.Product).filter(models.Product.name == data["name"]).first()
    if exist_name:
        raise HTTPException(status_code=400, detail="Tên sản phẩm đã tồn tại!")

    # Nếu không trùng → thêm sản phẩm
    new_product = models.Product(**data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# UPDATE
@router.put("/{product_id}")
def update_product(product_id: int, data: dict, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# DELETE
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Deleted"}
