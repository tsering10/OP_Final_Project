from django.urls import path
from .views import RegisterUserView

urlpatterns = [
    path("registerUser/", RegisterUserView.as_view(), name='registerUser'),
]