from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://mongo_orders:27017"
DATABASE_NAME = "ecommerce_orders"

_client = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client

def get_db():
    client = get_client()
    return client[DATABASE_NAME]
