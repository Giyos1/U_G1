from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def time_default():
    return timezone.now() + timedelta(seconds=45)


class Code(models.Model):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_user')
    expired_data = models.DateTimeField(default=time_default)
