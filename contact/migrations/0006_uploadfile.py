# Generated by Django 5.1.6 on 2025-03-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_alter_contact_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='upload_file/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
