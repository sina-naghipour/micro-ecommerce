from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from ..db.db import get_db
from ..db.models import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])
db = get_db()


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    """Create a new order."""
    order_data = order.model_dump()
    result = db.orders.insert_one(order_data)
    created_order = db.orders.find_one({"_id": result.inserted_id})
    created_order["_id"] = str(created_order["_id"])
    return created_order


@router.get("/", response_model=list[OrderOut])
def list_orders():
    """List all orders."""
    orders = []
    for order in db.orders.find():
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: str):
    """Retrieve a specific order by ID."""
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order ID")

    order = db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    order["_id"] = str(order["_id"])
    return order
