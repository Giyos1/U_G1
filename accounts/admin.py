from django.contrib import admin
from django.contrib.auth.models import Permission
from accounts.models import User


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active")
