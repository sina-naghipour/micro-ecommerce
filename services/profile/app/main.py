from fastapi import FastAPI
from app.routes.profile_routes import router
from app.db.db import init_db

app = FastAPI(title="Profile Service", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()
