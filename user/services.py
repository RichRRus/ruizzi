from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from advertisement.models import ViewedAd
from user.models import User, UserPoints


class UserService:

    @staticmethod
    def __validate_password(password):
        errors = []
        password_validators = get_default_password_validators()
        for validator in password_validators:
            try:
                validator.validate(password, None)
            except DjangoValidationError as error:
                errors.extend(error.messages)
        if errors:
            raise ValidationError(errors)

    @staticmethod
    def create_user(*, email: str, password: str, **extra_fields) -> User:
        email = UserManager.normalize_email(email)
        UserService.__validate_password(password)
        with transaction.atomic():
            user = User(email=email, username=email, **extra_fields)
            user.password = make_password(password)
            user.save()
            UserPoints.objects.create(
                user=user,
            )
            ViewedAd.objects.create(
                user=user,
            )
        return user
