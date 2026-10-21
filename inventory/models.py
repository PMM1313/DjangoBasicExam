


from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import transaction


class Category(models.Model):

    name = models.CharField(max_length=100,
        unique=True,
        error_messages={
            "unique": "Category already exists.",
        },
        help_text="Enter a unique name for this equipment category.",
    )

    description = models.TextField(blank=True,
        help_text="details about category.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Equipment(models.Model):

    name = models.CharField(max_length=150)
    serial_number = models.CharField(max_length=100,unique=True,
        help_text="Enter the unique serial number of the equipment.",
    )

    category = models.ForeignKey(Category,on_delete=models.PROTECT,
        related_name="equipment",
    )

    # kolichestvo v palni edinici
    # eventualen use case 1 kutiq sas 100 bolcheta ?!?

    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Current quantity in stock.",
    )

    minimum_stock = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Show a low-stock warning when quantity is below this value.",
    )

    # eventualen use case 1 kutiq sas 100 bolcheta ?!?
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    suppliers = models.ManyToManyField(
        "suppliers.Supplier",
        blank=True,
        related_name="equipment",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    @property
    def is_low_stock(self):
        return self.quantity < self.minimum_stock


class StockMovement(models.Model):

    class MovementType(models.TextChoices):
        RECEIVED = "received", "Stock received"
        REMOVED = "removed", "Stock removed"

    equipment = models.ForeignKey(Equipment,on_delete=models.PROTECT,related_name="stock_movements")

    movement_type = models.CharField(max_length=10,choices=MovementType.choices)

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    reason = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return (
            f"{self.get_movement_type_display()} - " # ot django
            f"{self.equipment.name}: {self.quantity}")

    def save(self, *args, **kwargs):

        # za showcase
        if self.pk is not None:
            raise ValidationError(
                "Existing stock movements cannot be edited. "
                "Create a new movement to correct the stock."
            )

        if self.quantity < 1:
            raise ValidationError(
                {"quantity": "Quantity must be at least 1."})

        with transaction.atomic():
            equipment = Equipment.objects.select_for_update().get(pk=self.equipment_id)

            if self.movement_type == self.MovementType.REMOVED:
                if self.quantity > equipment.quantity:
                    raise ValidationError({
                        "quantity": (
                            f"Only {equipment.quantity} items "
                            "are currently available."
                        )
                    })

                equipment.quantity -= self.quantity

            elif self.movement_type == self.MovementType.RECEIVED:
                equipment.quantity += self.quantity

            else:
                raise ValidationError({
                    "movement_type": "Select a valid movement type."
                })

            equipment.save(update_fields=["quantity"])
            self.equipment = equipment
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        # Reverse before deleation.
        with transaction.atomic():
            equipment = Equipment.objects.select_for_update().get(pk=self.equipment_id)

            if self.movement_type == self.MovementType.RECEIVED:
                if equipment.quantity < self.quantity:
                    raise ValidationError(
                        "This movement cannot be deleted because "
                        "there is not enough stock to reverse it."
                    )
                equipment.quantity -= self.quantity

            elif self.movement_type == self.MovementType.REMOVED:
                equipment.quantity += self.quantity

            equipment.save(update_fields=["quantity"])

            return super().delete(*args, **kwargs)


