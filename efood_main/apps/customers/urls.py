from django.urls import path

from efood_main.apps.accounts import views as account_views

from . import views

urlpatterns = [
    path("", account_views.CustDashboardView.as_view(), name="customer"),
    path(
        "booking-confirmation",
        views.WorkshopBookConfirmation.as_view(),
        name="workshop-confirmation",
    ),
    path("c-profile/", views.CustomerProfileView.as_view(), name="cust_profile"),
    path(
        "workshop/",
        views.CustomerBookedWorkshopsView.as_view(),
        name="customer_workshop",
    ),
    path(
        "workshop-detail/<int:id>",
        views.CustomerWorkshopDetail.as_view(),
        name="cust-workshop-detail",
    ),
    path(
        "workshop/<int:workshop_id>/book/",
        views.CustWorkshopBook.as_view(),
        name="book-workshop",
    ),
]
