from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.db import transaction

from user.models import User, UserPoints


class UserService:

    @staticmethod
    def create_user(*, email: str, password: str, **extra_fields) -> User:
        email = UserManager.normalize_email(email)
        with transaction.atomic():
            user = User(email=email, username=email, **extra_fields)
            user.password = make_password(password)
            user.save()
            UserPoints.objects.create(
                user=user,
            )
        return user
