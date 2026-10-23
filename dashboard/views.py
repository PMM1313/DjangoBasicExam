from django.shortcuts import render

from decimal import Decimal

from django.db.models import F, Sum
from django.shortcuts import render

from inventory.models import Category, Equipment
from suppliers.models import Supplier
from maintenance.models import RepairRecord


def home(request):
    low_stock_items = Equipment.objects.filter(
        quantity__lt=F("minimum_stock")
    )

    total_maintenance_cost = (
        RepairRecord.objects.aggregate(
            total=Sum("repair_cost")
        )["total"]
        or Decimal("0.00")
    )

    context = {
        "category_count": Category.objects.count(),
        "equipment_count": Equipment.objects.count(),
        "stock_quantity": sum(
            Equipment.objects.values_list("quantity", flat=True)
        ),
        "supplier_count": Supplier.objects.count(),
        "low_stock_count": low_stock_items.count(),
        "low_stock_items": low_stock_items.select_related("category")[:5],
        "open_repairs_count": RepairRecord.objects.exclude(
            status=RepairRecord.Status.COMPLETED
        ).count(),
        "total_maintenance_cost": total_maintenance_cost,
    }

    return render(request, "dashboard/home.html", context)
