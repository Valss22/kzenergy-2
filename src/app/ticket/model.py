import datetime
from tortoise import models, fields

from src.app.ticket.types import AggregateState, MeasureSystem, WasteDestinationType, TicketStatus


class Ticket(models.Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    wasteName = fields.CharField(max_length=50)
    facility = fields.ForeignKeyField("models.Facility")
    wasteDestinationType = fields.CharEnumField(WasteDestinationType)
    aggregateState = fields.CharEnumField(AggregateState)
    user = fields.ForeignKeyField("models.User")
    measureSystem = fields.CharEnumField(MeasureSystem)
    quantity = fields.FloatField()
    archived = fields.BooleanField(default=False)
    status = fields.CharEnumField(TicketStatus, default=TicketStatus.PENDING.value)
    report = fields.ForeignKeyField("models.Report", related_name="tickets", null=True)
    excelUrl = fields.CharField(max_length=150, null=True)
    message = fields.CharField(max_length=200, null=True)
    usedInReport = fields.BooleanField(default=False)