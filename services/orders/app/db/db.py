from pymongo import MongoClient

MONGO_URL = "mongodb://mongo_orders:27017"
DATABASE_NAME = "ecommerce_orders"

_client = None


def get_client() -> MongoClient:
    """Return a global MongoDB client."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URL)
    return _client


def get_db():
    """Return the database object."""
    client = get_client()
    return client[DATABASE_NAME]
