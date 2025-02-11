# Generated by Django 5.1.6 on 2025-02-06 15:28

import book.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, validators=[book.models.validate_full_name])),
                ('birth_date', models.DateField()),
                ('phone_number', models.CharField(max_length=13)),
                ('nationality', models.CharField(max_length=50)),
                ('gender', models.CharField(default='m|f', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('publish_date', models.DateField(default=django.utils.timezone.now)),
                ('price', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='book.author')),
            ],
        ),
    ]
