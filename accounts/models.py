from datetime import timedelta

import pyotp
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group

from common.models import Base


class UserRole(models.TextChoices):
    ADMIN = ('admin', 'Admin')
    Client = ('client', 'Client')
    MANAGER = ('manager', 'Manager')


class User(AbstractUser):
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255, choices=UserRole.choices, default=UserRole.Client)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    is_2fa_enabled = models.BooleanField(default=False)  # 2FA yoqilganmi?
    totp_secret = models.CharField(max_length=32, blank=True, null=True)

    # def contact_count(self):
    #     return self.user_contact.all().count()

    def generate_otc(self):
        self.totp_secret = pyotp.random_base32()
        self.save()

    def verify_otp(self, otp):
        if not self.totp_secret:
            return False
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(otp, valid_window=3)

    def __str__(self):
        return self.get_full_name()


def time_default():
    return timezone.now() + timedelta(seconds=45)


class Code(models.Model):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_user')
    expired_data = models.DateTimeField(default=time_default)


class Transaction(Base):
    from_acc = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='from_acc_trans', null=True)
    to_acc = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='to_acc_trans', null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'transaction'
        ordering = ('-created_at',)
