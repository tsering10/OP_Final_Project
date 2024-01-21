from django.urls import path

from efood_main.apps.accounts import views as account_views

from . import views

urlpatterns = [
    path("", account_views.CustDashboardView.as_view(), name="chef"),
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
    path(
        "recipe-builder/category/edit/<int:pk>/",
        views.EditCategoryView.as_view(),
        name="edit_category",
    ),
    path(
        "recipe-builder/category/delete/<int:pk>/",
        views.CategoryDeleteView.as_view(),
        name="delete_category",
    ),
    # RecipeItem CRUD
    path(
        "recipe-builder/recipe/add/", views.AddRecipeView.as_view(), name="add_recipe"
    ),
    path(
        "recipe-builder/recipe/edit/<int:pk>/",
        views.EditRecipeView.as_view(),
        name="edit_recipe",
    ),
    path(
        "recipe-builder/recipe/delete/<int:pk>/",
        views.RecipeDeleteView.as_view(),
        name="delete_recipe",
    ),
    path(
        "recipe-builder/recipe/<str:slug>/<int:id>/",
        views.RecipeDetailView.as_view(),
        name="recipe_detail",
    ),
    # Workshop CRUD
    path(
        "workshop-builder/",
        views.ChefWorkshopBuilder.as_view(),
        name="workshop_builder",
    ),
    path(
        "workshop-builder/workshop/add/",
        views.AddWorkshopView.as_view(),
        name="add_workshop",
    ),
    path(
        "workshop-builder/workshop/edit/<int:pk>/",
        views.EditWorkshopView.as_view(),
        name="edit_workshop",
    ),
    path(
        "workshop-builder/workshop/delete/<int:pk>/",
        views.WorkshopDeleteView.as_view(),
        name="delete_workshop",
    ),
    path(
        "workshop-builder/workshop/<int:id>/",
        views.WorkshopDetailView.as_view(),
        name="workshop_detail",
    ),
]
