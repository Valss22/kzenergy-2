import datetime
from tortoise import models, fields

from src.app.report.model import Report


class SummaryReport(models.Model):
    id = fields.UUIDField(pk=True)
    date = fields.DateField(default=datetime.date.today())
    user = fields.ForeignKeyField("models.User")
    excel = fields.CharField(max_length=150, null=True)
    reports: fields.ReverseRelation['Report']
