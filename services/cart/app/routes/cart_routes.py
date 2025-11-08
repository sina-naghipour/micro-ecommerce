from fastapi import APIRouter, Depends, HTTPException
from app.db.redis_client import r
from app.authentication.auth import verify_token

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/health", tags=["Health"])
async def health():
    return {"status": "cart ok"}

@router.post("/add")
async def add_to_cart(item_id: str, quantity: int, user=Depends(verify_token)):
    """
    Add item to user's cart.
    """
    key = f"cart:{user['token']}"
    await r.hincrby(key, item_id, quantity)
    return {"message": f"{quantity} of item {item_id} added to cart"}

@router.post("/remove")
async def remove_from_cart(item_id: str, user=Depends(verify_token)):
    """
    Remove item from user's cart.
    """
    key = f"cart:{user['token']}"
    await r.hdel(key, item_id)
    return {"message": f"Item {item_id} removed from cart"}

@router.get("/")
async def get_cart(user=Depends(verify_token)):
    """
    Get all items in user's cart.
    """
    key = f"cart:{user['token']}"
    cart = await r.hgetall(key)
    return {"cart": cart}

