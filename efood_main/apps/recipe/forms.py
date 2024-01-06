from django import forms
from .models import Category, RecipeItem
from efood_main.apps.accounts.validator import custom_validator
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_duration


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class DurationFormField(forms.DurationField):
    def to_python(self, value):
        try:
            return parse_duration(value)
        except ValueError:
            raise ValidationError("Enter a valid duration in the format 'hh:mm:ss'.")


class RecipeItemForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info w-100"}),
        validators=[custom_validator],
    )
    preparation_time = DurationFormField()

    class Meta:
        model = RecipeItem
        fields = [
            "category",
            "recipe_title",
            "recipe_ingredients",
            "recipe_instructions",
            "preparation_time",
            "external_link",
            "image",
        ]
