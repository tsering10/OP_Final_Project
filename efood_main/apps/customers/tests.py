from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from efood_main.apps.accounts.forms import UserInfoForm, UserProfileForm
from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.customers.views import CustomerViewMixin


class CustomerViewMixinTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            first_name="john",
            last_name="doe",
            email="testuser@example.com",
            password="test1234",
            is_active=True,
            role=2,
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def test_customer_user(self):
        # Attach the is_customer attribute to simulate a customer
        self.user.role = User.CUSTOMER
        self.user.save()

        request = HttpRequest()
        request.user = self.user

        mixin = CustomerViewMixin()
        mixin.request = request

        # Test the customer case
        self.assertTrue(mixin.test_func(), "test_func should return True for customers")

    def test_non_customer_user(self):
        # Set the user's role to CHEF
        self.user.role = User.CHEF
        self.user.save()

        request = HttpRequest()
        request.user = self.user

        mixin = CustomerViewMixin()
        mixin.request = request

        # Test the non-customer case
        self.assertFalse(
            mixin.test_func(), "test_func should return False for non-customers"
        )


class CustomerProfileViewTest(TestCase):
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create(
            username="testuser",
            first_name="john",
            last_name="doe",
            email="testuser@example.com",
            password="test1234",
            is_active=True,
            role=2,
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("cust_profile"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("cust_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/customer_profile.html")
        self.assertIsInstance(
            response.context["combined_form"]["profile_form"], UserProfileForm
        )
        self.assertIsInstance(
            response.context["combined_form"]["user_form"], UserInfoForm
        )


class CustomerWorkshopBookTest(TestCase):
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create(
            username="testuser",
            first_name="henry",
            last_name="doe",
            email="testuser@example.com",
            password="test12345",
            is_active=True,
            role=2,
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def test_customer_book_workshop(self):
        response = self.client.get(reverse("customer_workshop"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/customer_workshop.html")

    def test_workshop_book_confirmation(self):
        response = self.client.get(reverse("workshop-confirmation"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/booking-confirmation.html")
