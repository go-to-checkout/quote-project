from tortoise import fields, models
class Diary(models.Model):
    id = fields.UUIDField(pk=True)
    user_id = fields.UUIDField(index=True)
    title = fields.CharField(200, null=True)
    content = fields.TextField()
    class Meta: table = "diaries"
