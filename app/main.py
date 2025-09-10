from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.db import TORTOISE_ORM
from app.api.v1 import auth as auth_router

app = FastAPI(title="My Diary API")
app.include_router(auth_router.router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
