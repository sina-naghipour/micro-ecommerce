from app.repositories.cart_repository import CartRepository

class CartService:
    @staticmethod
    async def add_to_cart(user_id: str, item_id: str, quantity: int):
        await CartRepository.add_item(user_id, item_id, quantity)
        return {"message": f"{quantity} of item {item_id} added to cart"}

    @staticmethod
    async def remove_from_cart(user_id: str, item_id: str):
        await CartRepository.remove_item(user_id, item_id)
        return {"message": f"Item {item_id} removed from cart"}

    @staticmethod
    async def get_cart(user_id: str):
        cart = await CartRepository.get_cart(user_id)
        return {"cart": cart}
