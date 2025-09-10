# app/models/user.py
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, null=True)
    password_hash = fields.CharField(max_length=255)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username or f"User({self.id})"


class TokenBlacklist(Model):
    token_blacklist_id = fields.IntField(pk=True)  # 실제 테이블의 PK 필드명
    user_id = fields.IntField()
    token = fields.TextField()
    expired_at = fields.DatetimeField()

    class Meta:
        table = "token_blacklist"

    def __str__(self):
        return f"TokenBlacklist(user={self.user_id})"
