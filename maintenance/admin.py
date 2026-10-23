from django.contrib import admin


from django.contrib import admin

from .models import RepairRecord


@admin.register(RepairRecord)
class RepairRecordAdmin(admin.ModelAdmin):
    list_display = (
        "equipment",
        "status",
        "date_reported",
        "date_completed",
        "repair_cost",
    )
    list_filter = (
        "status",
        "date_reported",
        "date_completed",
    )
    search_fields = (
        "equipment__name",
        "equipment__serial_number",
        "problem_description",
        "repair_notes",
    )
    list_select_related = ("equipment",)
    readonly_fields = ("date_reported",)
    date_hierarchy = "date_reported"

