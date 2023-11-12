from django.urls import path
from .views import RegisterUserView, RegisterChefView

urlpatterns = [
    path("registerUser/", RegisterUserView.as_view(), name="registerUser"),
    path("registerChef/", RegisterChefView.as_view(), name="registerChef"),
]
