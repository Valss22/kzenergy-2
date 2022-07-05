import datetime

from tortoise import models, fields

from src.app.ticket.model import Ticket


class Report(models.Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    archived = fields.BooleanField(default=False)
    user = fields.ForeignKeyField("models.User")
    tickets: fields.ReverseRelation['Ticket']
