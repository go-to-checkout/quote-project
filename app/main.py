from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.db.database import setup_database

app = FastAPI(title="PostgreSQL + TortoiseORM API")

# 데이터베이스 설정
setup_database(app)

# 라우터 등록
app.include_router(users_router, prefix="/api", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello FastAPI + PostgreSQL + TortoiseORM!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
