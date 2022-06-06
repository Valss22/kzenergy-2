from tortoise import fields, models
from src.app.user.types import Roles


class User(models.Model):
    id = fields.UUIDField(pk=True)
    fullname = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    role = fields.CharEnumField(Roles)
    password_hash = fields.BinaryField()
    phone = fields.CharField(max_length=15)
