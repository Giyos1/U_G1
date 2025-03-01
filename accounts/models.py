from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings


class UserRoles(models.TextChoices):
    ADMIN = "Admin", "Admin"
    MANAGER = "Manager", "Manager"
    USER = "User", "User"


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


def time_default():
    return timezone.now() + timedelta(seconds=45)


class Code(models.Model):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expired_data = models.DateTimeField(default=time_default)
