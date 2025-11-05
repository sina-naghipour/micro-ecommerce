from fastapi import FastAPI
from .routes.order_routes import router

app = FastAPI(title="Orders Service", version="1.0.0")
app.include_router(router)
