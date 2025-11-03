from fastapi import FastAPI
from .routes.product_routes import router
from .db.db import init_db

app = FastAPI(title="Products Service")

app.include_router(router, prefix="/products", tags=["Products"])

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
async def health():
    return {"status": "ok"}
