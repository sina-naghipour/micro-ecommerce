from fastapi import FastAPI
from .routes.product_routes import router
from .db.db import init_db

app = FastAPI(title="Products Service", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()
