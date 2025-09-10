from tortoise import fields
from tortoise.models import Model


class Diary(Model):
    """일기 모델 - ERD diaries 테이블"""

    diary_id = fields.IntField(pk=True)  # 일기 고유 ID
    user_id = fields.IntField()  # 사용자 고유 ID (단순 정수 필드)
    title = fields.CharField(max_length=255)  # 일기 제목 (NOT NULL)
    content = fields.CharField(max_length=1000)  # 일기 내용 (NOT NULL)
    created_at = fields.DatetimeField()  # 작성일시

    class Meta:
        table = "diaries"

    def __str__(self):
        return self.title
