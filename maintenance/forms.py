
from django import forms
from .models import RepairRecord

class RepairRecordForm(forms.ModelForm):

    class Meta:

        model = RepairRecord

        fields = [
            "equipment",
            "problem_description",
            "repair_notes",
            "status",
            "date_completed",
            "repair_cost"]

        widgets = {

            "equipment": forms.Select(),

            "problem_description": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the equipment problem",}),

            "repair_notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the repair work performed",}),

            "status": forms.Select(),

            "date_completed": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),

            "repair_cost": forms.NumberInput(attrs={"min": 0, "step": "0.01"})}

        help_texts = {
            "status": "reported, in progress, or completed ",
            "date_completed":  "when status is completed",
            "repair_cost": "cost",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_completed"].input_formats = ["%Y-%m-%d"]
