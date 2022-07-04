import datetime

from tortoise import models, fields

from src.app.ticket.model import Ticket


class Report(models.Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    archived = fields.BooleanField(default=False)
    excel_url = fields.CharField(max_length=150)
    tickets: fields.ReverseRelation['Ticket']
