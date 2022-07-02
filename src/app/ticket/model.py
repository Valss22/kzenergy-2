from tortoise import models, fields

from src.app.ticket.types import AggregateState


class Ticket(models.Model):
    id = fields.UUIDField(pk=True)
    aggregate_state = fields.CharEnumField(AggregateState)
    density = fields.FloatField()
