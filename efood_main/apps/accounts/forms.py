from django import forms
from .models import User, UserProfile
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CUSTOMER
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


def custom_validator(value):
    valid_formats = ["png", "jpeg"]
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f"{value.name} is not a valid image format")


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[custom_validator],
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"})
    )

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "city",
            "country",
            "state",
            "postal_code",
        ]
