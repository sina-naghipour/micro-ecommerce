from fastapi import APIRouter, Depends, HTTPException
from app.authentication.auth import verify_token
from app.services.cart_service import CartService
from app.models.cart_models import AddToCartRequest, RemoveFromCartRequest
import logging
import asyncio

router = APIRouter(prefix="/cart", tags=["Cart"])

logger = logging.getLogger("cart_routes")
logging.basicConfig(level=logging.INFO)

@router.get("/health", tags=["Health"])
async def health():
    from app.db.redis_client import r
    try:
        pong = await asyncio.wait_for(r.ping(), timeout=1.0)
        return {"status": "ok" if pong else "redis down"}
    except Exception:
        raise HTTPException(503, "Redis service unavailable")

@router.post("/add")
async def add_to_cart(request: AddToCartRequest, user=Depends(verify_token)):
    user_id = user.get("token")
    response = await CartService.add_to_cart(user_id, request.item_id, request.quantity)
    logger.info(f"Added item {request.item_id} x{request.quantity} for user {user_id}")
    return response

@router.post("/remove")
async def remove_from_cart(request: RemoveFromCartRequest, user=Depends(verify_token)):
    user_id = user.get("token")
    response = await CartService.remove_from_cart(user_id, request.item_id)
    logger.info(f"Removed item {request.item_id} for user {user_id}")
    return response

@router.get("/")
async def get_cart(user=Depends(verify_token)):
    user_id = user.get("token")
    response = await CartService.get_cart(user_id)
    logger.info(f"Retrieved cart for user {user_id}")
    return response
