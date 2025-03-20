import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from common.models import Base, Deleted
from django.utils.translation import gettext_lazy as _


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def search(self, q):
        return self.filter(name__icontains=q)


class Contact(Deleted, Base):
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(_("phone"), max_length=20)
    address = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contact')

    objects = CustomManager()
    all_manager = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "contact"
        ordering = ["-created_at"]


# def upload_to_dynamic(instance, filename):
#     model_name = instance.type
#     return os.path.join(f"{model_name}/", f"{timezone.now().date()}_{filename}")


class UploadFile(Base):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='upload_file/')
