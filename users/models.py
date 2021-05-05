from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .generate_code import generate_confirmation_code


class User(AbstractUser):
    ROLES_CHOICES = [
        (settings.USER, 'user'),
        (settings.MODERATOR, 'moderator'),
        (settings.ADMIN, 'admin'),
    ]

    bio = models.CharField(
        max_length=1000,
        null=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Код подтверждения',
        default=generate_confirmation_code()
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES_CHOICES,
        default=settings.USER,
        verbose_name='Роль'
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return self.is_staff or self.role == settings.ADMIN

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR
