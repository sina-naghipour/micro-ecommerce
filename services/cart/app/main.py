from fastapi import FastAPI
from .routes.cart_routes import router

app = FastAPI(title="Cart Service", version="1.0.0")

app.include_router(router)

