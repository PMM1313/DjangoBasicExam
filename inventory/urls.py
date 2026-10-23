from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.index, name="index"),

    # categories
    path("categories/", views.category_list, name="categories"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    # equipment
    path("equipment/add/", views.equipment_create, name="equipment_create"),
    path("equipment/<int:pk>/edit/", views.equipment_update, name="equipment_update"),
    path("equipment/<int:pk>/delete/", views.equipment_delete, name="equipment_delete"),

    # Stock movement
    path("stock-movements/", views.stock_movement_list, name="stock_movements"),
    path("stock-movements/add/", views.stock_movement_create, name="stock_movement_create"),
    path("stock-movements/<int:pk>/delete/", views.stock_movement_delete, name="stock_movement_delete"),
]