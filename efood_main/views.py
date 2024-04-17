from django.db.models import Q
from django.views.generic import ListView

from efood_main.apps.recipe.models import RecipeItem


class HomePageView(ListView):
    model = RecipeItem
    template_name = "home.html"
    context_object_name = "recipe_items"
    queryset = RecipeItem.objects.all().order_by("created_at")[:4]


class RecipeSearchListView(ListView):
    model = RecipeItem
    template_name = "recipe_search_results.html"
    context_object_name = "search_recipes"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return RecipeItem.objects.filter(
                Q(recipe_title__icontains=query)
                | Q(recipe_ingredients__icontains=query)
                | Q(category__category_name__icontains=query)
            ).distinct()
        else:
            return RecipeItem.objects.none()
