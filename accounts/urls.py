from django.urls import path, include
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('django/', include('django.contrib.auth.urls')),
    path("register/", views.register, name='register'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("profile/", views.profile, name='profile'),
    path("profile/edit/", views.profile_edit, name='profile_edit'),
    path('forget_password/', views.forgot_password, name='forgot_password'),
    path('restore_password/', views.restore_password, name='restore_password')
]
