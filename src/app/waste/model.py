from tortoise import fields, models

from src.app.waste.types import AggregateState


class Waste(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    type = fields.CharEnumField(AggregateState)
    density = fields.FloatField()
