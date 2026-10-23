from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:

        model = Supplier

        fields = ["name", "contact_person", "email", "phone", "address",]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Supplies OOD."}),
            "contact_person": forms.TextInput(attrs={"placeholder": "Contact person"}),
            "email": forms.EmailInput(attrs={"placeholder": "supplier@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Address",}),
        }