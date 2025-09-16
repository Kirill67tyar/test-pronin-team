from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        blank=False,
        unique=True,
        verbose_name="email",
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name="Фамилия",
    )

    class Meta:
        ordering = (
            "username",
            "-date_joined",
        )

    def __str__(self):
        return f"username: {self.username}"
