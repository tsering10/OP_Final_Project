from django import forms
from .models import Chef


class ChefForm(forms.ModelForm):
    chef_license = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"})
    )

    class Meta:
        model = Chef
        fields = ["chef_name", "chef_license"]
