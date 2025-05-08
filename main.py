from typing import Union

from fastapi import FastAPI

from app.db import init_db
from app.router import router



app = FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()

app.include_router(router)

