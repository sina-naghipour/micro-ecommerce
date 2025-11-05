from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.db import get_db
from ..db.models import Product
from ..authentication.auth import verify_token
from pydantic import BaseModel
from typing import Optional


router = APIRouter(prefix="/products", tags=["Products"])


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True


@router.post("/", response_model=ProductOut, dependencies=[Depends(verify_token)])
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.get("/", response_model=list[ProductOut], dependencies=[Depends(verify_token)])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()


@router.get("/health", tags=["Health"], dependencies=[Depends(verify_token)])
async def health():
    return {"status": "products ok"}


@router.get("/{product_id}", response_model=ProductOut, dependencies=[Depends(verify_token)])
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


