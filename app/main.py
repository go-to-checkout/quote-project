# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1.users import router as users_router  # 이 줄 제거
from app.api.v1 import auth, diary, question, quote
from app.db.database import setup_database

app = FastAPI(
    title="일기 관리 API",  # 제목도 더 명확하게 변경
    description="JWT 인증, 일기 작성, 명언 북마크, 자기성찰 질문 기능을 제공하는 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 설정 (프론트엔드 연동을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영에서는 구체적인 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 설정
setup_database(app)

# JWT 인증 기반 라우터들만 등록
app.include_router(auth.router, prefix="/api/v1")
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/v1")
app.include_router(question.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "일기 관리 API에 오신 것을 환영합니다!"}


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
