from fastapi import FastAPI
from .routes.auth_routes import router
from .db.db import init_db


app = FastAPI(title='Auth Service')

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router, prefix='/auth', tags=['Auth'])



