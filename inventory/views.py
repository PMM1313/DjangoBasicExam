from django.shortcuts import render

from django.db.models import Count, F

from .models import Category, Equipment


def index(request):

    equipment = Equipment.objects.select_related("category").prefetch_related("suppliers")

    low_stock_only = request.GET.get("low_stock") == "1"

    if low_stock_only:
        equipment = equipment.filter(quantity__lt=F("minimum_stock"))

    context = {
        "equipment_list": equipment,
        "low_stock_only": low_stock_only,
    }

    return render(request, "inventory/index.html", context)


def category_list(request):
    categories = Category.objects.annotate(equipment_count=Count("equipment"))

    context = {
        "categories": categories,
    }

    return render(request, "inventory/category_list.html", context)