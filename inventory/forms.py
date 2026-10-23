from django import forms
from .models import Category, Equipment, StockMovement


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "description"]  # it takes help_text from the model, maybe clutering the form
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. Power Tools",
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Optional category description",
            }),
        }

class EquipmentForm(forms.ModelForm):


    # serial number not editable when editing equipment
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["serial_number"].disabled = True

    class Meta:
        model = Equipment
        fields = [
            "name",
            "serial_number",
            "category",
            "minimum_stock",
            "unit_price",
            "suppliers",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "A Drill for example... :)",
            }),
            "serial_number": forms.TextInput(attrs={
                "placeholder": "Unique serial number",
            }),
            "category": forms.Select(),
            "minimum_stock": forms.NumberInput(attrs={
                "min": 1,
            }),
            "unit_price": forms.NumberInput(attrs={
                "min": 0,
                "step": "0.01",
            }),

            # not sure about this...
            "suppliers": forms.SelectMultiple(),
        }

        # widgets already have placeholder, maybe use only placeholder OR help_text will check how it looks
        # will leave it for now for showcase/test
        help_texts = {
            "serial_number": "Each equipment must have unique serial number.",
            "minimum_stock": "Show a low stock warning when stock falls bellow this quantity.",
            "suppliers": "You can select multiple choises.",
        }



class StockMovementForm(forms.ModelForm):

    class Meta:
        model = StockMovement
        fields = [
            "equipment",
            "movement_type",
            "quantity",
            "reason",
        ]
        widgets = {
            "equipment": forms.Select(),
            "movement_type": forms.Select(),
            "quantity": forms.NumberInput(attrs={"min": 1}),
            "reason": forms.TextInput(
                attrs={"placeholder": " reason for movement"}
            ),
        }
        help_texts = {
            "equipment": "Select equipment for change.",
            "quantity": "Enter a number greater than zero.",
            "reason": "Test .....",
        }