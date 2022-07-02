from tortoise import models, fields

from src.app.waste.types import AggregateState


class Ticket(models.Model):
    id = fields.UUIDField(pk=True)
    type = fields.CharEnumField(AggregateState)
    density = fields.FloatField()