from tortoise import fields, models


class Waste(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

