from fastapi import FastAPI
from .routes.profile_routes import router
from .db.db import init_db

app = FastAPI(title="Profile Service", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def startup():
    for route in app.routes:
        print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
    await init_db()
