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


class Contact(Deleted, Base):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='contact_image')
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contact')

    objects = CustomManager()
    all_manager = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "contact"
        ordering = ["-created_at"]


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')  # Fayllar "media/uploads/" ichida saqlanadi
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
