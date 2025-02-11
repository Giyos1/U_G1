from django.contrib import admin
from book.models import Book, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book)