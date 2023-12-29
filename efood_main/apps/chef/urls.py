from django.urls import path
from . import views
from efood_main.apps.accounts import views as AccountViews

urlpatterns = [
    path("", AccountViews.CustDashboardView.as_view(), name="chef"),
    path("profile/", views.ChefProfileView.as_view(), name="chef_profile"),
    path("recipe-builder/", views.ChefRecipeBuilder.as_view(), name="recipe_builder"),
    path(
        "recipe-builder/category/<int:pk>/",
        views.RecipeItemsByCategoryView.as_view(),
        name="recipeitems_by_category",
    ),
    path(
        "recipe-builder/category/add/",
        views.AddCategoryView.as_view(),
        name="add_category",
    ),
]
