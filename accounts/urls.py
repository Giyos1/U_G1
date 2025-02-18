from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("list/", views.user_list, name="list"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
]
