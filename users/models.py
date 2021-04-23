from django.contrib.auth.models import AbstractUser
from django.db import models
from .generate_code import generate_confirmation_code


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.CharField(
        max_length=1000,
        null=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=10,
        null=True,
        verbose_name='Код подтверждения',
        default=generate_confirmation_code()
    )
    role = models.CharField(
        max_length=50,
        choices=Roles.choices,
        verbose_name='Роль'
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return self.is_staff or self.role == Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR
