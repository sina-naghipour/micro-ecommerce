from pydantic import BaseModel

class AddToCartRequest(BaseModel):
    item_id: str
    quantity: int

class RemoveFromCartRequest(BaseModel):
    item_id: str

class CartItem(BaseModel):
    item_id: str
    quantity: int

class CartResponse(BaseModel):
    cart: dict[str, int]
