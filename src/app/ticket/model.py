from tortoise import models, fields

from src.app.ticket.types import AggregateState, MeasureSystem


class Ticket(models.Model):
    id = fields.UUIDField(pk=True)
    date_of_removal = fields.DateField()
    facility = fields.ForeignKeyField("models.Facility")
    waste_destination = fields.CharField(max_length=50)
    aggregate_state = fields.CharEnumField(AggregateState)
    worker = fields.ForeignKeyField("models.User")
    measure_system = fields.CharEnumField(MeasureSystem)
    quantity = fields.FloatField()
    archived = fields.BooleanField(default=False)
