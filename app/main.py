from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import products, dashboard, imports, export, inventory_check

# Tạo bảng
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(imports.router, prefix="/imports", tags=["Imports"])
app.include_router(export.router, prefix="/export", tags=["Export"]) 
app.include_router(inventory_check.router)

@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL OK!"}
