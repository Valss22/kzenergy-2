import datetime

from tortoise import models, fields

from src.app.ticket.model import Ticket


class Report(models.Model):
    tickets: fields.ReverseRelation['Ticket']
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    archived = fields.BooleanField(default=False)
