import datetime

from tortoise import models, fields

from src.app.ticket.types import AggregateState, MeasureSystem, WasteDestinationType, TicketStatus


class Ticket(models.Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    facility = fields.ForeignKeyField("models.Facility")
    waste_destination_type = fields.CharEnumField(WasteDestinationType)
    aggregate_state = fields.CharEnumField(AggregateState)
    worker = fields.ForeignKeyField("models.User")
    measure_system = fields.CharEnumField(MeasureSystem)
    quantity = fields.FloatField()
    archived = fields.BooleanField(default=False)
    status = fields.CharEnumField(TicketStatus, default=TicketStatus.PENDING.value)
    report = fields.ForeignKeyField("models.Report", related_name="tickets", null=True)
    excel_url = fields.CharField(max_length=150)
    message = fields.CharField(max_length=200, null=True)
