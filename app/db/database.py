# app/db/database.py
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

# 상대 경로 import 문제 해결
try:
    from .config import TORTOISE_CONFIG
except ImportError:
    # 상대 경로가 안 될 경우 절대 경로로
    from app.db.config import TORTOISE_CONFIG


async def init_db():
    """데이터베이스 초기화 (개발용)"""
    try:
        await Tortoise.init(config=TORTOISE_CONFIG)
        await Tortoise.generate_schemas()
        print("✅ 데이터베이스 초기화 완료")
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")
        raise


async def close_db():
    """데이터베이스 연결 종료"""
    try:
        await Tortoise.close_connections()
        print("✅ 데이터베이스 연결 종료")
    except Exception as e:
        print(f"❌ 데이터베이스 연결 종료 실패: {e}")


def setup_database(app: FastAPI, generate_schemas: bool = True):
    """FastAPI 앱에 TortoiseORM 등록"""
    try:
        register_tortoise(
            app,
            config=TORTOISE_CONFIG,
            generate_schemas=generate_schemas,  # 개발용은 True, 운영용은 False
            add_exception_handlers=True,
        )
        print("✅ TortoiseORM 등록 완료")
    except Exception as e:
        print(f"❌ TortoiseORM 등록 실패: {e}")
        raise


# 선택적: 직접 실행을 위한 테스트 함수
async def test_connection():
    """데이터베이스 연결 테스트"""
    try:
        await init_db()
        print("🎉 데이터베이스 연결 테스트 성공!")
        return True
    except Exception as e:
        print(f"💥 데이터베이스 연결 테스트 실패: {e}")
        return False
    finally:
        await close_db()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_connection())
