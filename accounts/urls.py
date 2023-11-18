from django.urls import path
from . import views


urlpatterns = [
    path("registerUser/", views.RegisterUserView.as_view(), name="registerUser"),
    path("registerChef/", views.RegisterChefView.as_view(), name="registerChef"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "customer/dashboard/",
        views.CustomerDashboardView.as_view(),
        name="customerDashboard",
    ),
    path(
        "chef/dashboard/",
        views.ChefDashboardView.as_view(),
        name="chefDashboard",
    ),
]
