from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,Group

class UserRole(models.TextChoices):
    ADMIN = ('admin', 'Admin')
    Client = ('client', 'Client')
    MANAGER = ('manager', 'Manager')


class User(AbstractUser):
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255, choices=UserRole.choices, default=UserRole.Client)

    # def contact_count(self):
    #     return self.user_contact.all().count()

    def __str__(self):
        return self.get_full_name()


def time_default():
    return timezone.now() + timedelta(seconds=45)


class Code(models.Model):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_user')
    expired_data = models.DateTimeField(default=time_default)
