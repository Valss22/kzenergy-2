from tortoise import fields, models

from src.app.waste.types import TypesOfWaste


class Waste(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    type = fields.CharEnumField(TypesOfWaste)
    density = fields.FloatField()
