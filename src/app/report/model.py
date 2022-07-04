import datetime

from tortoise import models, fields


class Report(models.Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    archived = fields.BooleanField(default=False)
