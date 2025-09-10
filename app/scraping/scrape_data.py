import asyncio
import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

try:
    # 상대 경로로 import 시도
    from .question_scraper import QuestionScraper, QuestionSeeder
    from .quote_scraper import QuoteScraper
except ImportError:
    # 절대 경로로 import
    from app.db.database import close_db, init_db
    from app.scraping.question_scraper import QuestionScraper, QuestionSeeder
    from app.scraping.quote_scraper import QuoteScraper


async def main():
    """메인 스크래핑 실행 함수"""
    print("🚀 Selenium을 사용한 데이터 스크래핑 및 시드 시작!")

    # 데이터베이스 초기화
    print("🔗 데이터베이스 연결 중...")
    await init_db()

    try:
        # 1. 명언 스크래핑 (Selenium 사용)
        print("\n" + "=" * 60)
        print("📚 Selenium으로 명언 스크래핑 시작...")
        print("=" * 60)

        with QuoteScraper(
            headless=True
        ) as scraper:  # headless=False로 설정하면 브라우저 창이 보입니다
            quotes = scraper.scrape_quotes(max_pages=3)  # 3페이지 스크래핑
            print(f"📊 총 {len(quotes)}개의 명언을 수집했습니다.")

            if quotes:
                saved_count = await scraper.save_quotes_to_db(quotes)
                print(f"💾 {saved_count}개의 새로운 명언이 데이터베이스에 저장되었습니다.")
            else:
                print("⚠️ 수집된 명언이 없습니다.")

        # 2. 자기성찰 질문 스크래핑 (새로운 QuestionScraper 사용)
        print("\n" + "=" * 60)
        print("❓ 자기성찰 질문 스크래핑 시작...")
        print("=" * 60)

        with QuestionScraper(headless=True) as question_scraper:
            questions = question_scraper.scrape_questions()

            if questions:
                question_count = await question_scraper.save_questions_to_db(questions)
                print(f"💾 {question_count}개의 새로운 질문이 데이터베이스에 저장되었습니다.")
            else:
                print("⚠️ 수집된 질문이 없습니다.")

                # 백업용 기본 질문 시드
                print("\n📝 백업용 기본 질문 시드 실행...")
                backup_count = await QuestionSeeder.seed_questions()
                print(f"💾 {backup_count}개의 기본 질문이 데이터베이스에 저장되었습니다.")

        print("\n" + "=" * 60)
        print("🎉 모든 데이터 스크래핑 및 시드가 완료되었습니다!")
        print("=" * 60)
        print("✨ 이제 FastAPI 서버를 실행하여 API를 테스트해보세요!")
        print("🔗 서버 실행: python main.py")
        print("📖 API 문서: http://localhost:8000/docs")

    except Exception as e:
        print(f"❌ 스크래핑 중 오류 발생: {e}")
        import traceback

        traceback.print_exc()

        # 오류 발생 시 백업용 기본 데이터 시드
        try:
            print("\n🔄 오류 발생으로 인한 백업 데이터 시드 실행...")
            backup_count = await QuestionSeeder.seed_questions()
            print(f"💾 {backup_count}개의 기본 질문이 백업으로 저장되었습니다.")
        except Exception as backup_error:
            print(f"❌ 백업 데이터 시드도 실패: {backup_error}")

    finally:
        # 데이터베이스 연결 종료
        await close_db()
        print("\n🔚 데이터베이스 연결이 종료되었습니다.")


if __name__ == "__main__":
    asyncio.run(main())
