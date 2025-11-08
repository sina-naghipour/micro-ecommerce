from fastapi import FastAPI
from app.routes.order_routes import router
import logging

app = FastAPI(title="Orders Service", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orders_service")

app.include_router(router, prefix='/orders', tags=['Orders'])
