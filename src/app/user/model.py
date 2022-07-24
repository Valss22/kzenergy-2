from tortoise import fields, models
from src.app.user.permission.model import Permission
from src.app.user.types import UserRole


class User(models.Model):
    id = fields.UUIDField(pk=True)
    fullname = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    role = fields.CharEnumField(UserRole)
    password_hash: bytes = fields.BinaryField()
    phone = fields.CharField(max_length=15)
    permission: fields.ReverseRelation["Permission"]