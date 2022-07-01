from tortoise import fields, models


class Facility(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    wastes = fields.ManyToManyField("models.Waste")

