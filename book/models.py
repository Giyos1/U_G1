from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Category(models.TextChoices):
    BADIIY = ("badiiy", 'Badiiy')
    ILMIY = ("ilmiy", 'Ilmiy')


def validate_full_name(value):
    if len(value) < 1:
        raise ValidationError('Please enter a valid full name')


class Author(models.Model):
    full_name = models.CharField(max_length=50, validators=[validate_full_name])
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=13)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books')
    description = models.TextField(null=True, blank=True)
    publish_date = models.DateField(default=timezone.now)
    # price = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.IntegerField(default=0)
    category = models.CharField(choices=Category.choices, max_length=20, default=Category.BADIIY)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
