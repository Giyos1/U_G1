from django.urls import path

from . import views

app_name = "contacts"
urlpatterns = [
    # path('admin/dashboard', views.dashboard, name='dashboard'),
    path("list/", views.contact_list, name="contact_list"),
    path("create/", views.contact_create, name="contact_create"),
    path("create/form/", views.contact_create_form, name="contact_create_form"),
    path("edit/<int:pk>/", views.contact_edit, name="contact_edit"),
    path("delete/<int:pk>/", views.contact_delete, name="contact_delete"),
    path("detail/<int:pk>/", views.contact_detail, name="contact_detail"),

]
