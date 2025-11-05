
import os

# === CLEAN CODE MICROSERVICES GENERATOR ===
# Generates: orders (Mongo, async) and products (Postgres, async SQLAlchemy)

services = {
    "orders": {
        "app/db/db.py": '''from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://mongo_orders:27017"
DATABASE_NAME = "ecommerce_orders"

_client = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client

def get_db():
    client = get_client()
    return client[DATABASE_NAME]
''',

        "app/db/models.py": '''from pydantic import BaseModel, EmailStr, Field

class OrderBase(BaseModel):
    customer_email: EmailStr
    product_name: str
    amount: float

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        from_attributes = True
''',

        "app/routes/order_routes.py": '''from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from ..db.db import get_db
from ..db.models import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    db = get_db()
    order_data = order.model_dump()
    result = await db.orders.insert_one(order_data)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    created_order["_id"] = str(created_order["_id"])
    return created_order

@router.get("/", response_model=list[OrderOut])
async def list_orders():
    db = get_db()
    orders = []
    async for order in db.orders.find():
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")

    db = get_db()
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["_id"] = str(order["_id"])
    return order
''',

        "app/main.py": '''from fastapi import FastAPI
from .routes.order_routes import router

app = FastAPI(title="Orders Service", version="1.0.0")
app.include_router(router)

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
''',

        "requirements.txt": "fastapi\nuvicorn\nmotor\npydantic[email]\n",
        "Dockerfile": '''FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
'''
    },

    "products": {
        "app/db/db.py": '''from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:toor@db_products:5432/ecommerce_products"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
''',

        "app/db/models.py": '''from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
''',

        "app/routes/product_routes.py": '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.db import get_db
from ..db.models import Product
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

@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
''',

        "app/main.py": '''from fastapi import FastAPI
from .routes.product_routes import router
from .db.db import init_db

app = FastAPI(title="Products Service", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
''',

        "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\nasyncpg\npydantic\n",
        "Dockerfile": '''FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
'''
    }
}

# === GENERATE FILES ===
for service, files in services.items():
    for path, content in files.items():
        file_path = os.path.join(service, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Async 'orders' (Mongo) and 'products' (Postgres) microservices created successfully with clean structure!")
