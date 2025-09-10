from tortoise import fields, models
class RevokedToken(models.Model):
    id = fields.IntField(pk=True)
    jti = fields.CharField(50, unique=True, index=True)
    expires_at = fields.DatetimeField()
    class Meta: table = "revoked_tokens"
