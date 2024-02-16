from django.views.generic import ListView

from efood_main.apps.recipe.models import RecipeItem


class HomePageView(ListView):
    model = RecipeItem
    template_name = "home.html"
    context_object_name = "recipe_items"
    queryset = RecipeItem.objects.all().order_by("created_at")[:4]
