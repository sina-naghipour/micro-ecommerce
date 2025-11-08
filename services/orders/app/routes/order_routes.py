from fastapi import APIRouter, Depends, HTTPException, status
from app.authentication.auth import verify_token
from app.services.order_service import OrderService
from app.db.models import OrderCreate, OrderOut
import logging

router = APIRouter()
logger = logging.getLogger("order_routes")
logging.basicConfig(level=logging.INFO)

@router.get("/health", tags=["Health"])
async def health():
    return {"status": "orders ok"}

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def create_order(order: OrderCreate):
    order_data = order.model_dump()
    created_order = await OrderService.create_order(order_data)
    logger.info(f"Created order {created_order['_id']} for {created_order['customer_email']}")
    return created_order

@router.get("/", response_model=list[OrderOut], dependencies=[Depends(verify_token)])
async def list_orders():
    orders = await OrderService.list_orders()
    logger.info(f"Retrieved {len(orders)} orders")
    return orders

@router.get("/{order_id}", response_model=OrderOut, dependencies=[Depends(verify_token)])
async def get_order(order_id: str):
    order = await OrderService.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    logger.info(f"Retrieved order {order_id}")
    return order
