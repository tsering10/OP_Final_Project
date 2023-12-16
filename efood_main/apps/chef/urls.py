from django.urls import path
from . import views
from efood_main.apps.accounts import views as AccountViews

urlpatterns = [
    path("", AccountViews.CustDashboardView.as_view(), name="chef"),
    path("profile/", views.ChefProfileView.as_view(), name="chef_profile"),
]
