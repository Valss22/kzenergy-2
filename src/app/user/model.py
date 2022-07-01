from tortoise import fields, models
from src.app.user.types import Role


class User(models.Model):
    id = fields.UUIDField(pk=True)
    fullname = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    role = fields.CharEnumField(Role)
    password_hash: bytes = fields.BinaryField()
    phone = fields.CharField(max_length=15)
