from fastapi import FastAPI
from .routes.order_routes import router as order_router

app = FastAPI(title="Orders Service", version="1.0.0")

app.include_router(order_router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
