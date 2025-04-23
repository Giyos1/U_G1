from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('login/google/', views.google_login, name='google_login'),
    path('google/callback', views.google_callback, name='google_callback'),
    path('2fa/', views.two_factor_auth, name='2fa'),
    path('admin/dashboard', views.dashboard, name='dashboard'),
    path("register/", views.register, name='register'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("profile/", views.profile, name='profile'),
    path("profile/edit/", views.profile_edit, name='profile_edit'),
    path('forget_password/', views.forgot_password, name='forgot_password'),
    path('restore_password/', views.restore_password, name='restore_password'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('session/', views.session_data_get_decode, name='session')
]
