from django.contrib import admin
from .models import Category, RecipeItem

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ("category_name", "chef", "updated_at")
    search_fields = ("category_name", "chef__chef_name")


class RecipeItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("recipe_title",)}
    list_display = ("recipe_title", "category", "chef", "updated_at")
    search_fields = ("recipe_title", "category__category_name", "chef__chef_name")


admin.site.register(Category, CategoryAdmin)
admin.site.register(RecipeItem, RecipeItemAdmin)
