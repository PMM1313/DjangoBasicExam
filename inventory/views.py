from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from .forms import CategoryForm, EquipmentForm, StockMovementForm
from django.db.models import Count, F

from .models import Category, Equipment, StockMovement


# loaded at first
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

# only category
def category_list(request):
    categories = Category.objects.annotate(equipment_count=Count("equipment"))

    context = {
        "categories": categories,}

    return render(request, "inventory/category_list.html", context)




################ CRUD CATEGORY #########################

def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("inventory:categories")
    else:
        form = CategoryForm()

    context = {
        "form": form,
        "page_title": "Add Category",
    }

    return render(request, "inventory/category_form.html", context)


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("inventory:categories")
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "page_title": "Edit Category",
    }

    return render(request, "inventory/category_form.html", context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        try:
            category.delete()
            messages.success(request, "Category deleted successfully.")
        except ProtectedError:
            messages.error(
                request,
                "This category cannot be deleted because equipment "
                "is assigned to it.",
            )

        return redirect("inventory:categories")

    return render(
        request,
        "inventory/category_confirm_delete.html",
        {"category": category},
    )

################# END CRUD CATEGORY ######################




################# CRUD EQUIPMENT ##########################

def equipment_create(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Equipment added successfully.",
            )
            return redirect("inventory:index")
    else:
        form = EquipmentForm()

    return render(
        request,
        "inventory/equipment_form.html",
        {
            "form": form,
            "page_title": "Add Equipment",
        },
    )


def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Equipment updated successfully.",
            )
            return redirect("inventory:index")
    else:
        form = EquipmentForm(instance=equipment)

    return render(
        request,
        "inventory/equipment_form.html",
        {
            "form": form,
            "page_title": "Edit Equipment",
            "equipment": equipment,
        },
    )


def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == "POST":
        try:
            equipment.delete()
            messages.success(
                request,
                "Equipment deleted successfully.",
            )
        except ProtectedError:
            messages.error(
                request,
                "This equipment cannot be deleted because related "
                "stock movements or repair records exist.",
            )

        return redirect("inventory:index")

    return render(
        request,
        "inventory/equipment_confirm_delete.html",
        {"equipment": equipment},
    )

############### END OF CRUD EQUIPMENT ################################




################ STOCK MOVEMENT #######################################

def stock_movement_list(request):
    movements = StockMovement.objects.select_related(
        "equipment"
    )

    return render(
        request,
        "inventory/stock_movement_list.html",
        {"movements": movements},
    )

def stock_movement_create(request):
    if request.method == "POST":
        form = StockMovementForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Stock movement recorded successfully.",
                )
                return redirect("inventory:stock_movements")

            except ValidationError as error:
                form.add_error(None, error)

    else:
        form = StockMovementForm()

    return render(
        request,
        "inventory/stock_movement_form.html",
        {
            "form": form,
            "page_title": "Record Stock Movement",
        },
    )

def stock_movement_delete(request, pk):
    movement = get_object_or_404(StockMovement, pk=pk)

    if request.method == "POST":
        try:
            movement.delete()
            messages.success(
                request,
                "Stock movement deleted and stock adjusted.",
            )
        except ValidationError as error:
            messages.error(request, error)

        return redirect("inventory:stock_movements")

    return render(
        request,
        "inventory/stock_movement_confirm_delete.html",
        {"movement": movement},
    )

##################### END OF STOCK MOVEMENT ##########################