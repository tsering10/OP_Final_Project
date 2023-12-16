from django.urls import path, include
from .views import (
    RegisterChefView,
    RegisterUserView,
    LoginView,
    LogoutView,
    ChefDashboardView,
    CustDashboardView,
    ActivateView,
    ForgotPasswordView,
    ResetPasswordValidateView,
    ResetPasswordView,
)


urlpatterns = [
    path("registerUser/", RegisterUserView.as_view(), name="registerUser"),
    path("registerChef/", RegisterChefView.as_view(), name="registerChef"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "customerDashboard/",
        CustDashboardView.as_view(),
        name="customerDashboard",
    ),
    path(
        "chefDashboard/",
        ChefDashboardView.as_view(),
        name="chefDashboard",
    ),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("forgot_password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        ResetPasswordValidateView.as_view(),
        name="reset_password_validate",
    ),
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password"),
    path("chef/", include("efood_main.apps.chef.urls")),
]
