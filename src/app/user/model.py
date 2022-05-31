import bcrypt
from tortoise import fields, models

from src.app.user.types import Roles
from src.app.settings import SALT


class User(models.Model):
    id = fields.UUIDField(pk=True)
    fullname = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    role = fields.CharEnumField(Roles)
    password_hash = fields.BinaryField()
    phone = fields.CharField(max_length=15)

    async def save(self, *args, **kwargs):
        self.password_hash = bcrypt.hashpw(self.password_hash, SALT)
        await super().save(*args, **kwargs)
