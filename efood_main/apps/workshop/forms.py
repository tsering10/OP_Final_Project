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
        ]
