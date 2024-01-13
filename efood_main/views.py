from django.views.generic import TemplateView, ListView
from efood_main.apps.recipe.models import RecipeItem


class HomePageView(ListView):
    model = RecipeItem
    template_name = "home.html"


# class SearchResultsView(ListView):
#     model = RecipeItem
#     template_name = "home.html"
