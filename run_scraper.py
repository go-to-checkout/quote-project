import asyncio
import os
import sys

# 현재 파일의 디렉토리를 기준으로 프로젝트 루트 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


async def main():
    # 간단한 테스트부터 시작
    print("🚀 스크래핑 도구 시작!")
    print(f"📁 현재 작업 디렉토리: {os.getcwd()}")
    print(f"📂 스크립트 위치: {current_dir}")

    # 필요한 모듈들이 있는지 확인
    try:
        print("📦 모듈 확인 중...")

        from app.db.database import close_db, init_db

        print("✅ 데이터베이스 모듈 OK")

        from app.models.quote import Quote

        print("✅ Quote 모델 OK")

        from app.models.question import Question

        print("✅ Question 모델 OK")

        # 데이터베이스 연결 테스트
        await init_db()
        quote_count = await Quote.all().count()
        question_count = await Question.all().count()
        await close_db()

        print(f"📊 현재 명언 {quote_count}개, 질문 {question_count}개")
        print("🎉 모든 기본 모듈이 정상입니다!")

        if quote_count == 0 or question_count == 0:
            print("💡 스크래핑을 실행하여 데이터를 추가할 수 있습니다.")
            print("📝 설치 명령: pip install selenium webdriver-manager")

    except ImportError as e:
        print(f"❌ 모듈 import 오류: {e}")
        print("💡 확인사항:")
        print("   1. app 폴더 구조가 올바른지 확인")
        print("   2. __init__.py 파일들이 있는지 확인")
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")


if __name__ == "__main__":
    asyncio.run(main())
