from django.urls import path
from .views import (
    RegisterChefView,
    RegisterUserView,
    LoginView,
    LogoutView,
    ChefDashboardView,
    CustDashboardView,
    ActivateView,
)


urlpatterns = [
    path("registerUser/", RegisterUserView.as_view(), name="registerUser"),
    path("registerChef/", RegisterChefView.as_view(), name="registerChef"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "customer/dashboard/",
        CustDashboardView.as_view(),
        name="customerDashboard",
    ),
    path(
        "chef/dashboard/",
        ChefDashboardView.as_view(),
        name="chefDashboard",
    ),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
]
