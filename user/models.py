from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from user.utils.manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Middle name')
    phone = PhoneNumberField(verbose_name='Phone')
    location = models.CharField(max_length=511, blank=True, verbose_name='Location')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        full_name = f'{self.last_name} {self.first_name} {self.middle_name}'
        return full_name.strip()

    def __str__(self):
        return f'{str(self.get_full_name())} : {str(self.email)}'


class UserPoints(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='points',
                             verbose_name='Пользователь')
    amount = models.FloatField(verbose_name='Количество', default=0.0)

    class Meta:
        verbose_name = 'Баллы пользователя'
        verbose_name_plural = 'Баллы пользователей'
        constraints = [
            models.UniqueConstraint('user', name='unique_user')
        ]

    def __str__(self):
        return str(self.user)
