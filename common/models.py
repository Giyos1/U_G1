from django.db import models
from django.db.models import Manager


class BaseQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class DeleteManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return BaseQuerySet(self.model).filter(is_deleted=True)


class Base(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Deleted(models.Model):
    is_deleted = models.BooleanField(default=False)

    all_object = Manager()
    objects = DeleteManager()

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.is_deleted = True
        self.save()
