from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from ..db.db import get_db
from ..authentication.auth import verify_token
from ..db.models import OrderCreate, OrderOut


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def create_order(order: OrderCreate):
    db = get_db()
    order_data = order.model_dump()
    result = await db.orders.insert_one(order_data)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    created_order["_id"] = str(created_order["_id"])
    return created_order


@router.get("/", response_model=list[OrderOut], dependencies=[Depends(verify_token)])
async def list_orders():
    db = get_db()
    orders = []
    async for order in db.orders.find():
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders


@router.get("/health", tags=["Health"], dependencies=[Depends(verify_token)])
async def health():
    return {"status": "orders ok"}


@router.get("/{order_id}", response_model=OrderOut, dependencies=[Depends(verify_token)])
async def get_order(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")

    db = get_db()
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["_id"] = str(order["_id"])
    return order



