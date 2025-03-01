from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from common.models import Base, Deleted
from config.settings import BASE_DIR


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def search(self, q):
        return self.filter(name__icontains=q)


class Contact(Deleted,Base):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contact')

    objects = CustomManager()
    all_manager = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "contact"
        ordering = ["-created_at"]
