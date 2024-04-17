from django import forms

from .models import Workshop


class WorkshopItemForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = [
            "title",
            "description",
            "date",
            "time",
            "capacity",
            "address",
            "latitude",
            "longitude",
            "price",
            "contact_phone",
            "recipe",
            # "chef",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, chef, *args, **kwargs):
        super(WorkshopItemForm, self).__init__(*args, **kwargs)
        self.fields["recipe"].queryset = chef.recipeitem_set.all()
