from app.db.db import get_db
from bson import ObjectId

class OrderRepository:
    @staticmethod
    async def create_order(order_data: dict):
        db = get_db()
        result = await db.orders.insert_one(order_data)
        return await db.orders.find_one({"_id": result.inserted_id})

    @staticmethod
    async def get_order(order_id: str):
        db = get_db()
        if not ObjectId.is_valid(order_id):
            return None
        return await db.orders.find_one({"_id": ObjectId(order_id)})

    @staticmethod
    async def list_orders():
        db = get_db()
        orders = []
        async for order in db.orders.find():
            orders.append(order)
        return orders
