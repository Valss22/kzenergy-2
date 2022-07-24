from tortoise import fields, models


class Permission(models.Model):
    id = fields.UUIDField(pk=True)
    write = fields.BooleanField(default=True)
    read = fields.BooleanField(default=True)
    temporary = fields.BooleanField(default=False)
    user = fields.OneToOneField("models.User", related_name="permission")
  