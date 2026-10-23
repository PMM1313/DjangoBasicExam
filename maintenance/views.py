
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RepairRecordForm
from .models import RepairRecord


def index(request):
    repairs = RepairRecord.objects.select_related("equipment")

    return render(
        request,
        "maintenance/index.html",
        {"repairs": repairs},
    )


def repair_create(request):
    if request.method == "POST":
        form = RepairRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Repair record created successfully.")
            return redirect("maintenance:index")
    else:
        form = RepairRecordForm()

    return render(
        request,
        "maintenance/repair_form.html",
        {
            "form": form,
            "page_title": "Report Equipment Problem",
        },
    )


def repair_update(request, pk):
    repair = get_object_or_404(RepairRecord, pk=pk)

    if request.method == "POST":
        form = RepairRecordForm(request.POST, instance=repair)

        if form.is_valid():
            form.save()
            messages.success(request, "Repair record updated successfully.")
            return redirect("maintenance:index")
    else:
        form = RepairRecordForm(instance=repair)

    return render(
        request,
        "maintenance/repair_form.html",
        {
            "form": form,
            "page_title": "Edit Repair Record",
            "repair": repair,
        },
    )


def repair_delete(request, pk):
    repair = get_object_or_404(RepairRecord, pk=pk)

    if request.method == "POST":
        repair.delete()
        messages.success(request, "Repair record deleted successfully.")
        return redirect("maintenance:index")

    return render(
        request,
        "maintenance/repair_confirm_delete.html",
        {"repair": repair},
    )

