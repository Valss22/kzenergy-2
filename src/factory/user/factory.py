import factory
from src.app.user.model import User


class UserFactory(factory.Factory):
    email = "test2@gmail.com"

    class Meta:
        model = User

