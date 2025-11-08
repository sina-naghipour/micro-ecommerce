from fastapi import FastAPI
from app.routes import cart_routes
from app.core.config import settings
import logging

app = FastAPI(title="Cart Service", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cart_service")

# Include routes
app.include_router(cart_routes.router)
