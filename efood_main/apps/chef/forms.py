from django import forms
from .models import Chef


class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ["chef_name", "chef_license"]
