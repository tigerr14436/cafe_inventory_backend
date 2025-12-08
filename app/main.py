from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import products, dashboard, imports

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

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(imports.router, prefix="/imports", tags=["Imports"])

@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL OK!"}
