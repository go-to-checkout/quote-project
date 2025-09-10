# app/db/config.py
import os
from typing import Any, Dict

try:
    from dotenv import load_dotenv

    load_dotenv()
    print("✅ .env 파일 로드됨")
except ImportError:
    print("⚠️ python-dotenv 패키지가 설치되지 않았습니다")
    print("설치: pip install python-dotenv")

# 환경변수에서 DATABASE_URL 읽기
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://postgres:password@localhost:5432/fastapi_db",  # 기본값
)

# 개별 DB 정보도 읽기 (백업용)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")

# DATABASE_URL이 제대로 설정되지 않은 경우 개별 정보로 생성
if DATABASE_URL == ("postgres://postgres:password@localhost:5432/fastapi_db"):
    DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}" f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔗 사용할 DATABASE_URL: {DATABASE_URL.replace(DB_PASSWORD, '***')}")

TORTOISE_CONFIG: Dict[str, Any] = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                # ERD에 맞게 모든 모델 추가
                "app.models.user",  # User, TokenBlacklist
                "app.models.diary",  # Diary
                "app.models.quote",  # Quote, Bookmark
                "app.models.question",  # Question, UserQuestion
                "aerich.models",  # 마이그레이션용
            ],
            "default_connection": "default",
        }
    },
    "use_tz": True,  # 타임존 사용
    "timezone": "Asia/Seoul",  # 한국 시간대
}
AERICH_CONFIG = {
    "tortoise_orm": TORTOISE_CONFIG,
    "location": "./app/db/migrations",  # 📁 마이그레이션 파일 저장 경로
    "src_folder": "./app",  # 📂 소스 코드 폴더
}


# 설정 확인을 위한 함수
def print_config():
    """현재 설정 출력 (디버깅용)"""
    print("📋 현재 TortoiseORM 설정:")
    print(f"  - DATABASE_URL: {DATABASE_URL.replace(DB_PASSWORD, '***')}")
    print(f"  - Models: {TORTOISE_CONFIG['apps']['models']['models']}")
    print(f"  - Timezone: {TORTOISE_CONFIG['timezone']}")


if __name__ == "__main__":
    print_config()
