from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("profile/", views.profile, name='profile'),
    path("profile/edit/", views.profile_edit, name='profile_edit')
]
