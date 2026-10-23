from django.shortcuts import render

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SupplierForm
from .models import Supplier


def index(request):

    suppliers = Supplier.objects.annotate(equipment_count=Count("equipment", distinct=True))

    return render(request, "suppliers/index.html", {"suppliers": suppliers})


def supplier_create(request):

    if request.method == "POST":

        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully.")
            return redirect("suppliers:index")
    else:

        form = SupplierForm()

    return render(request, "suppliers/supplier_form.html", {"form": form, "page_title": "Add Supplier"})


def supplier_update(request, pk):

    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":

        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():

            form.save()
            messages.success(request, "Supplier updated successfully.")
            return redirect("suppliers:index")
    else:

        form = SupplierForm(instance=supplier)

    return render(request,"suppliers/supplier_form.html", {"form": form, "page_title": "Edit Supplier", "supplier": supplier})


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":

        # Many to many relation. manual check for deleting

        if supplier.equipment.exists():
            messages.error(
                request,
                "Supplier cannot be deleted because it is assigned to equipment."
                "Remove the supplier from that equipment first.",
            )
        else:
            supplier.delete()
            messages.success(request, "Supplier deleted successfully.")

        return redirect("suppliers:index")

    return render(request, "suppliers/supplier_confirm_delete.html", {"supplier": supplier})