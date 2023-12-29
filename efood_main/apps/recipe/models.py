from django.db import models
from efood_main.apps.chef.models import Chef

# Create your models here.


class Category(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name


class RecipeItem(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="recipeitems"
    )
    recipe_title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    recipe_ingredients = models.TextField()
    recipe_instructions = models.TextField()
    preparation_time = models.DurationField()
    image = models.ImageField(upload_to="recipe_images/", null=True, blank=True)
    external_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe_title
