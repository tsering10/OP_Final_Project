from django.db import models
from efood_main.apps.chef.models import Chef
from efood_main.apps.accounts.models import User
from efood_main.apps.recipe.models import RecipeItem
from djmoney.models.fields import MoneyField


# Create your models here.
class Workshop(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, related_name="workshops")
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    capacity = models.IntegerField()
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    price = MoneyField(
        max_digits=10, decimal_places=2, default_currency="EUR", null=True
    )
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe = models.ForeignKey(
        RecipeItem, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class WorkshopRegistration(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    is_canceled = models.BooleanField(default=False)
