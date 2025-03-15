from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import User
from accounts.service import send_email_async_welcome


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created:
        send_email_async_welcome(
            to=instance.email,
        )


@receiver(pre_save, sender=User)
def user_balance(sender, instance, **kwargs):
    if not instance.id:
        print('malumot qoshilyapti')
    else:
        print('update bolyapti')

