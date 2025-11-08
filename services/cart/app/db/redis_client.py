import os
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://cart_redis:6379/0")

r = redis.from_url(REDIS_URL, decode_responses=True)
