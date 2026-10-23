from django.urls import path
from . import views

app_name = "maintenance"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.repair_create, name="repair_create"),
    path("<int:pk>/edit/", views.repair_update, name="repair_update"),
    path("<int:pk>/delete/", views.repair_delete, name="repair_delete"),
]