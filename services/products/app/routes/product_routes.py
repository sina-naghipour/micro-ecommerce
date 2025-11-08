from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.db import get_db
from app.db.models import Product
from app.authentication.auth import verify_token
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter(prefix="/products", tags=["Products"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("product_routes")

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True

@router.get("/health", tags=["Health"])
async def health():
    return {"status": "products ok"}

@router.post("/", response_model=ProductOut, dependencies=[Depends(verify_token)])
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    logger.info(f"Created product {new_product.name} (id={new_product.id})")
    return new_product

@router.get("/", response_model=list[ProductOut], dependencies=[Depends(verify_token)])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

@router.get("/{product_id}", response_model=ProductOut, dependencies=[Depends(verify_token)])
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
