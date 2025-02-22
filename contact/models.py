from django.contrib.auth.models import User
from django.db import models


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def search(self, q):
        return self.filter(name__icontains=q)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contact')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = CustomManager()
    all_manager = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "contact"
        ordering = ["-created_at"]
