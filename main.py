from typing import Union

from fastapi import FastAPI

from app.db import init_db

from db

@app.on_event("startup")
async def start_db():
    await init_db()

app = FastAPI()

app.include_router(router)

