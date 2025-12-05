from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(tags=["Products"])

# -------------------------------
# GET ALL PRODUCTS
# -------------------------------
@router.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

# -------------------------------
# GET PRODUCT BY ID
# -------------------------------
@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product

# -------------------------------
# CREATE PRODUCT
# -------------------------------
@router.post("/products")
def create_product(data: dict, db: Session = Depends(get_db)):
    new_product = models.Product(**data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# -------------------------------
# UPDATE PRODUCT
# -------------------------------
@router.put("/products/{product_id}")
def update_product(product_id: int, data: dict, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# -------------------------------
# DELETE PRODUCT
# -------------------------------
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Deleted"}
