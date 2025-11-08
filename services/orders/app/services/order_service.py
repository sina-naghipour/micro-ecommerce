from app.repositories.order_repository import OrderRepository

class OrderService:
    @staticmethod
    async def create_order(order_data: dict):
        order = await OrderRepository.create_order(order_data)
        order["_id"] = str(order["_id"])
        return order

    @staticmethod
    async def get_order(order_id: str):
        order = await OrderRepository.get_order(order_id)
        if order:
            order["_id"] = str(order["_id"])
        return order

    @staticmethod
    async def list_orders():
        orders = await OrderRepository.list_orders()
        for order in orders:
            order["_id"] = str(order["_id"])
        return orders
