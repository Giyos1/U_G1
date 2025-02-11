from django.urls import path

from . import views

app_name = 'contact'
urlpatterns = [
    path('', views.index, name='index'),
    path("about/", views.about, name="about"),
    # path("", views.book_list, name="book_list"),
    # path("<int:book_id>/", views.book_detail, name="book_detail"),
    # path("create/", views.book_create, name="book_create"),
]
