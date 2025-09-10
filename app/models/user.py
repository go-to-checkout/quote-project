from tortoise import fields, models
class User(models.Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True)
    password_hash = fields.CharField(255)
    nickname = fields.CharField(50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    class Meta: table = "users"
