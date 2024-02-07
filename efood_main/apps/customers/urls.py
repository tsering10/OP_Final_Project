from django.urls import path

from efood_main.apps.accounts import views as account_views

from . import views

urlpatterns = [
    path("", account_views.CustDashboardView.as_view(), name="customer"),
    path("c-profile/", views.CustomerProfileView.as_view(), name="cust_profile"),
    path(
        "workshop/",
        views.CustomerWorkshopsListView.as_view(),
        name="customer_workshop",
    ),
    path(
        "workshop-detail/<int:id>",
        views.CustomerWorkshopDetail.as_view(),
        name="cust-workshop-detail",
    ),
]
