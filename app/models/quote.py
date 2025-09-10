from tortoise import fields
from tortoise.models import Model


class Quote(Model):
    """명언 모델 - ERD quotes 테이블"""

    quote_id = fields.IntField(pk=True)  # 명언 고유 ID
    content = fields.TextField()  # 명언 내용 (NOT NULL)
    author = fields.CharField(max_length=50, null=True)  # 명언 작가 (NULL 허용)

    class Meta:
        table = "quotes"

    def __str__(self):
        return f"Quote by {self.author}"


class Bookmark(Model):
    """북마크 모델 - ERD bookmarks 테이블"""

    bookmark_id = fields.IntField(pk=True)  # 북마크 ID
    user_id = fields.IntField()  # 사용자 고유 ID (단순 정수 필드)
    quote_id = fields.IntField()  # 명언 고유 ID (단순 정수 필드)

    class Meta:
        table = "bookmarks"
        unique_together = (("user_id", "quote_id"),)  # 중복 북마크 방지

    def __str__(self):
        return f"Bookmark(user={self.user_id}, quote={self.quote_id})"
