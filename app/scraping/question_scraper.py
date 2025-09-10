import re
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from app.models.question import Question


class QuestionScraper:
    """Selenium을 사용한 자기성찰 질문 스크래핑 클래스"""

    def __init__(self, headless: bool = True):
        self.driver = None
        self.headless = headless
        self.wait = None

        # 스크래핑할 사이트들 (자기성찰 질문이 있는 사이트들)
        self.sites = [
            {
                "name": "365 Journal Prompts",
                "url": "https://www.signupgenius.com/groups/365-writing-prompts.cfm",
                "selector": "div.content p, div.content li",
            },
            {
                "name": "Self Reflection Questions",
                "url": "https://positivepsychology.com/introspection-self-reflection/",
                "selector": "li, h3 + p",
            },
        ]

    def setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        # 추가 옵션들
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        print("✅ Chrome 드라이버가 설정되었습니다.")

    def close_driver(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print("✅ Chrome 드라이버가 종료되었습니다.")

    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.setup_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.close_driver()

    def clean_question_text(self, text: str) -> str:
        """질문 텍스트 정리"""
        # 앞뒤 공백 제거
        text = text.strip()

        # 숫자나 불필요한 기호 제거 (예: "1. What is...", "• How do...")
        text = re.sub(r"^[\d\.\-\•\*\+\s]+", "", text)

        # 여러 공백을 하나로 변환
        text = re.sub(r"\s+", " ", text)

        # 질문이 아닌 것들 필터링
        if len(text) < 10 or len(text) > 200:  # 너무 짧거나 긴 텍스트 제외
            return None

        if not text.endswith("?"):  # 물음표로 끝나지 않는 텍스트 제외
            return None

        # 영어 질문을 한국어로 번역 (간단한 매핑)
        # translations = {
        #     "What": "무엇을",
        #     "How": "어떻게",
        #     "Why": "왜",
        #     "When": "언제",
        #     "Where": "어디서",
        #     "Who": "누가",
        #     "Which": "어떤",
        # }

        # 영어 질문 감지 및 제외 (한국어 질문만 수집하거나, 번역이 필요한 경우)
        if any(word in text for word in ["What", "How", "Why", "When", "Where", "Who"]):
            return None  # 영어 질문은 제외

        return text

    def scrape_custom_questions(self) -> List[str]:
        """커스텀 한국어 자기성찰 질문 생성"""
        korean_questions = [
            "오늘 나는 어떤 감정을 가장 많이 느꼈나요?",
            "지금 이 순간 내가 가장 원하는 것은 무엇인가요?",
            "최근에 내가 가장 자랑스러웠던 순간은 언제인가요?",
            "내가 스트레스를 받을 때 주로 어떻게 대처하나요?",
            "다른 사람들이 나를 어떻게 기억했으면 좋겠나요?",
            "내 인생에서 가장 중요한 가치는 무엇인가요?",
            "10년 후 내 모습은 어떨 것 같나요?",
            "내가 가장 편안함을 느끼는 장소는 어디인가요?",
            "지금까지 받은 조언 중 가장 도움이 된 것은 무엇인가요?",
            "내가 다른 사람에게 줄 수 있는 가장 큰 선물은 무엇인가요?",
            "어떤 일을 할 때 시간가는 줄 모르나요?",
            "내 삶에서 바꾸고 싶은 한 가지는 무엇인가요?",
            "가장 행복했던 기억을 떠올려보면 어떤 감정이 드나요?",
            "내가 두려워하는 것을 극복하려면 어떻게 해야 할까요?",
            "오늘 누군가에게 감사하고 싶은 일이 있었나요?",
            "내 강점과 약점을 한 문장으로 표현한다면?",
            "지금 내가 미루고 있는 일은 무엇인가요?",
            "내 인생의 멘토는 누구인가요? 그 이유는 무엇인가요?",
            "만약 실패에 대한 두려움이 없다면 무엇을 시도해보고 싶나요?",
            "내가 어린 시절 꿈꿨던 것 중 지금도 의미있는 것은 무엇인가요?",
            "다른 사람과 나를 비교할 때 어떤 감정이 드나요?",
            "내 삶의 균형을 위해 더 늘려야 할 것과 줄여야 할 것은?",
            "가장 창의적이라고 느끼는 순간은 언제인가요?",
            "내가 세상에 남기고 싶은 흔적은 무엇인가요?",
            "힘든 시기를 견뎌낼 수 있게 해주는 것은 무엇인가요?",
            "내 직감이 나를 올바른 방향으로 이끈 경험이 있나요?",
            "지금 내가 가장 감사해야 할 사람은 누구인가요?",
            "내 삶에서 가장 의미있는 관계는 무엇인가요?",
            "완벽하지 않은 나 자신을 받아들이기 위해 어떻게 해야 할까요?",
            "내가 진정으로 원하는 삶과 현재 살고 있는 삶의 차이는 무엇인가요?",
            "오늘 내가 배운 새로운 것이 있다면 무엇인가요?",
            "내 마음의 평화를 방해하는 요소들은 무엇인가요?",
            "가장 후회되는 일을 다시 할 수 있다면 어떻게 하고 싶나요?",
            "내가 진정으로 열정을 느끼는 일은 무엇인가요?",
            "다른 사람의 성공을 볼 때 어떤 감정이 드나요?",
            "내 삶에 더 많은 기쁨을 가져다줄 수 있는 작은 변화는 무엇일까요?",
            "내가 가장 존경하는 사람의 어떤 점을 닮고 싶나요?",
            "지금 내 에너지를 가장 많이 소모시키는 것은 무엇인가요?",
            "내가 다른 사람들에게 주는 첫인상은 어떨 것 같나요?",
            "혼자만의 시간을 보낼 때 주로 무엇을 하나요?",
        ]

        print(f"📝 {len(korean_questions)}개의 한국어 자기성찰 질문을 생성했습니다.")
        return korean_questions

    def scrape_philosophy_questions(self) -> List[str]:
        """철학적 사고를 위한 질문들"""
        philosophy_questions = [
            "행복이란 무엇이라고 생각하나요?",
            "성공의 진정한 의미는 무엇일까요?",
            "인간관계에서 가장 중요한 것은 무엇인가요?",
            "자유롭다는 것은 어떤 의미인가요?",
            "사랑과 좋아함의 차이는 무엇인가요?",
            "용기란 두려움이 없는 것일까요, 두려움을 극복하는 것일까요?",
            "완벽함을 추구하는 것이 항상 좋은 일일까요?",
            "다른 사람을 판단하지 않기 위해 어떻게 해야 할까요?",
            "실패가 성공보다 더 가치있을 때는 언제인가요?",
            "진정한 친구의 조건은 무엇이라고 생각하나요?",
            "나이가 들어간다는 것의 의미는 무엇일까요?",
            "돈과 행복의 관계에 대해 어떻게 생각하나요?",
            "용서한다는 것은 정확히 무엇을 의미할까요?",
            "개인의 성장과 안정 중 어느 것이 더 중요할까요?",
            "진실을 말하는 것이 항상 옳은 일일까요?",
        ]

        print(f"🤔 {len(philosophy_questions)}개의 철학적 질문을 생성했습니다.")
        return philosophy_questions

    def scrape_daily_reflection_questions(self) -> List[str]:
        """일상적 성찰을 위한 질문들"""
        daily_questions = [
            "오늘 하루 중 가장 기뻤던 순간은 언제였나요?",
            "오늘 내가 누군가에게 친절을 베푼 일이 있었나요?",
            "오늘 새롭게 배우거나 깨달은 것이 있나요?",
            "오늘 하루를 되돌아보며 후회되는 일이 있나요?",
            "오늘 나는 내 목표에 얼마나 가까워졌나요?",
            "오늘 가장 스트레스를 받은 순간과 그 이유는 무엇인가요?",
            "오늘 내가 도전한 새로운 일이 있었나요?",
            "오늘 누군가와 나눈 의미있는 대화가 있었나요?",
            "오늘 내 몸과 마음은 어떤 상태였나요?",
            "내일 더 나은 하루를 보내기 위해 무엇을 준비할 수 있을까요?",
            "오늘 감사했던 세 가지는 무엇인가요?",
            "오늘 내가 보인 최고의 모습은 언제였나요?",
            "오늘 예상과 다르게 흘러간 일이 있었나요?",
            "오늘 내 감정의 변화를 추적해보면 어떤 패턴이 있나요?",
            "오늘 가장 집중했던 일과 그때의 기분은 어땠나요?",
        ]

        print(f"📅 {len(daily_questions)}개의 일상 성찰 질문을 생성했습니다.")
        return daily_questions

    def scrape_questions(self) -> List[str]:
        """모든 질문 스크래핑 및 수집"""
        all_questions = []

        print("🚀 자기성찰 질문 수집을 시작합니다...")

        # 1. 커스텀 한국어 질문
        custom_questions = self.scrape_custom_questions()
        all_questions.extend(custom_questions)

        # 2. 철학적 질문
        philosophy_questions = self.scrape_philosophy_questions()
        all_questions.extend(philosophy_questions)

        # 3. 일상 성찰 질문
        daily_questions = self.scrape_daily_reflection_questions()
        all_questions.extend(daily_questions)

        # 중복 제거
        unique_questions = list(set(all_questions))

        print(f"\n🎉 총 {len(all_questions)}개의 질문을 수집했습니다.")
        print(f"📊 중복 제거 후 {len(unique_questions)}개의 고유한 질문이 남았습니다.")

        return unique_questions

    async def save_questions_to_db(self, questions: List[str]) -> int:
        """질문을 데이터베이스에 저장"""
        saved_count = 0

        print("\n💾 데이터베이스에 질문 저장 중...")

        for question_text in questions:
            try:
                # 중복 체크
                existing_question = await Question.filter(question_text=question_text).first()

                if not existing_question:
                    await Question.create(question_text=question_text)
                    saved_count += 1
                    print(f"✅ 질문 저장: {question_text}")
                else:
                    print(f"⏭️ 중복 질문 건너뜀: {question_text[:30]}...")

            except Exception as e:
                print(f"❌ 질문 저장 실패: {e}")
                continue

        print(f"\n🎊 {saved_count}개의 새로운 질문이 데이터베이스에 저장되었습니다!")
        return saved_count


# 기존 QuestionSeeder 클래스는 백업용으로 유지
class QuestionSeeder:
    """기본 자기성찰 질문 데이터 시드 클래스 (백업용)"""

    @staticmethod
    def get_sample_questions() -> List[str]:
        """기본 샘플 자기성찰 질문들"""
        return [
            "오늘 가장 감사했던 순간은 언제였나요?",
            "오늘 나는 어떤 감정을 가장 많이 느꼈나요?",
            "오늘 내가 가장 잘한 일은 무엇인가요?",
            "내일 더 나은 내가 되기 위해 무엇을 할 수 있을까요?",
            "오늘 배운 가장 중요한 교훈은 무엇인가요?",
        ]

    @staticmethod
    async def seed_questions() -> int:
        """기본 질문 데이터를 데이터베이스에 시드 (백업용)"""
        questions = QuestionSeeder.get_sample_questions()
        saved_count = 0

        for question_text in questions:
            try:
                existing_question = await Question.filter(question_text=question_text).first()

                if not existing_question:
                    await Question.create(question_text=question_text)
                    saved_count += 1
                    print(f"✅ 기본 질문 저장: {question_text}")
                else:
                    print(f"⏭️ 중복 질문 건너뜀: {question_text[:30]}...")

            except Exception as e:
                print(f"❌ 질문 저장 실패: {e}")
                continue

        return saved_count
