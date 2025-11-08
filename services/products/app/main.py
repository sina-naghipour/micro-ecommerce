from fastapi import FastAPI
from app.routes import product_routes
from app.db.db import init_db
import logging

app = FastAPI(title="Products Service", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("products_service")

# Include routes
app.include_router(product_routes.router)

@app.on_event("startup")
async def startup():
    await init_db()
    logger.info("Database initialized")
