from tortoise import fields
from tortoise.models import Model


class Question(Model):
    """질문 모델 - ERD questions 테이블"""

    question_id = fields.IntField(pk=True)  # 질문 고유 ID
    question_text = fields.TextField()  # 질문 내용 (NOT NULL)

    class Meta:
        table = "questions"

    def __str__(self):
        return f"Question({self.question_id})"


class UserQuestion(Model):
    """사용자 질문 이력 모델 - ERD user_questions 테이블"""

    user_question_id = fields.IntField(pk=True)  # 이력 ID
    user_id = fields.IntField()  # 사용자 고유 ID (단순 정수 필드)
    question_id = fields.IntField()  # 질문 고유 ID (단순 정수 필드)

    class Meta:
        table = "user_questions"

    def __str__(self):
        return f"UserQuestion(user={self.user_id}, question={self.question_id})"
