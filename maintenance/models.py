from django.db import models

from django.core.validators import MinValueValidator
from django.utils import timezone


class RepairRecord(models.Model):

    class Status(models.TextChoices):
        REPORTED = "reported", "Reported"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"

    equipment = models.ForeignKey(
        "inventory.Equipment", on_delete=models.PROTECT, related_name="repairs")

    problem_description = models.TextField()
    repair_notes = models.TextField(blank=True)
    date_reported = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True, blank=True)
    repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REPORTED
    )

    class Meta:
        ordering = ["-date_reported"]

    def __str__(self):
        return f"{self.equipment.name} - {self.get_status_display()}" # ot django

    def clean(self):
        super().clean()

        if self.date_completed and self.date_reported:
            if self.date_completed < self.date_reported:
                from django.core.exceptions import ValidationError
                raise ValidationError({
                    "date_completed": (
                        "Completion date cannot be before the report date."
                    )
                })

        if self.status == self.Status.COMPLETED and not self.date_completed:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                "date_completed": (
                    "Enter the completion date for a completed repair."
                )
            })

