from app.db.redis_client import r

class CartRepository:
    @staticmethod
    async def add_item(user_id: str, item_id: str, quantity: int):
        key = f"cart:{user_id}"
        await r.hincrby(key, item_id, quantity)

    @staticmethod
    async def remove_item(user_id: str, item_id: str):
        key = f"cart:{user_id}"
        await r.hdel(key, item_id)

    @staticmethod
    async def get_cart(user_id: str):
        key = f"cart:{user_id}"
        return await r.hgetall(key)
