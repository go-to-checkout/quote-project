from typing import List

from app.models.question import Question


class QuestionSeeder:
    """자기성찰 질문 데이터 시드 클래스"""

    @staticmethod
    def get_sample_questions() -> List[str]:
        """샘플 자기성찰 질문들"""
        return [
            "오늘 가장 감사했던 순간은 언제였나요?",
            "오늘 나는 어떤 감정을 가장 많이 느꼈나요?",
            "오늘 내가 가장 잘한 일은 무엇인가요?",
            "내일 더 나은 내가 되기 위해 무엇을 할 수 있을까요?",
            "오늘 배운 가장 중요한 교훈은 무엇인가요?",
            "지금 이 순간 내가 가장 원하는 것은 무엇인가요?",
            "오늘 누군가에게 도움이 된 일이 있었나요?",
            "내가 스트레스를 받았을 때 어떻게 해결했나요?",
            "오늘 나를 웃게 만든 것은 무엇이었나요?",
            "지금 내가 가장 집중해야 할 것은 무엇인가요?",
            "오늘 내가 실수한 것에서 무엇을 배웠나요?",
            "나는 어떤 순간에 가장 행복하다고 느끼나요?",
            "내가 다른 사람에게 영감을 줄 수 있는 방법은 무엇인가요?",
            "지금까지 살아오면서 가장 소중한 것은 무엇인가요?",
            "내가 두려워하는 것을 극복하기 위해 어떤 작은 단계를 밟을 수 있을까요?",
            "오늘 내가 가장 자랑스러웠던 순간은 언제였나요?",
            "내가 진정으로 원하는 삶의 모습은 어떤 것인가요?",
            "다른 사람의 어떤 점을 나도 본받고 싶나요?",
            "내가 가장 편안함을 느끼는 순간은 언제인가요?",
            "10년 후 나는 어떤 사람이 되어 있을까요?",
        ]

    @staticmethod
    async def seed_questions() -> int:
        """질문 데이터를 데이터베이스에 시드"""
        questions = QuestionSeeder.get_sample_questions()
        saved_count = 0

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

        return saved_count
