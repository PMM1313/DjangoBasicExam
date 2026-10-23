from django.contrib import admin


from django.contrib import admin

from .models import Category, Equipment, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "serial_number",
        "category",
        "quantity",
        "minimum_stock",
        "unit_price",
        "is_low_stock",
    )
    list_filter = ("category",)
    search_fields = ("name", "serial_number", "category__name")
    filter_horizontal = ("suppliers",)
    list_select_related = ("category",)
    readonly_fields = ("is_low_stock",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "equipment",
        "movement_type",
        "quantity",
        "reason",
        "date_created",
    )
    list_filter = ("movement_type", "date_created")
    search_fields = (
        "equipment__name",
        "equipment__serial_number",
        "reason",
    )
    list_select_related = ("equipment",)
    readonly_fields = (
        "equipment",
        "movement_type",
        "quantity",
        "reason",
        "date_created",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

