from django.contrib import admin
from contact.models import Contact, UploadFile


# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    pass
