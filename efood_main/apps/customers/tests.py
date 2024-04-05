from datetime import date, time

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from efood_main.apps.accounts.forms import UserInfoForm, UserProfileForm
from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.customers.views import CustomerViewMixin
from efood_main.apps.workshop.models import Workshop


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
        self.assertIn("combined_form", response.context_data)

    def test_post_with_valid_data_triggers_form_valid(self):
        # Prepare valid data for your UserProfileForm and UserInfoForm
        profile_picture = SimpleUploadedFile(
            "profile_pic.jpg", b"file_content", content_type="image/jpeg"
        )
        cover_photo = SimpleUploadedFile(
            "cover_photo.jpg", b"file_content", content_type="image/jpeg"
        )
        valid_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testupdate@example.com",
            "phone_number": "1234567890",
            "profile_picture": profile_picture,
            "cover_photo": cover_photo,
            "address": "123 Main St",
            "city": "Anytown",
            "country": "Country",
            "state": "State",
            "postal_code": "12345",
        }
        response = self.client.post(reverse("cust_profile"), data=valid_data)

        self.assertRedirects(response, reverse("customer"))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Profile updated.", [message.message for message in messages])
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")


class CustomerWorkshopDetailViewTest(TestCase):
    def setUp(self):
        self.chef = User.objects.create_user(
            username="chefuser",
            email="chef@example.com",
            password="chefpassword",
            first_name="Test",
            last_name="Chef",
        )

        # Create a user and profile
        self.customer = User.objects.create(
            username="testuser",
            first_name="henry",
            last_name="doe",
            email="testuser@example.com",
            password="test12345",
            is_active=True,
            role=2,
        )
        self.cust_profile, _ = UserProfile.objects.get_or_create(user=self.customer)
        self.chef_profile, _ = UserProfile.objects.get_or_create(user=self.chef)
        Chef.objects.create(
            user=self.chef, user_profile=self.chef_profile, chef_name="TestChef"
        )
        chef = Chef.objects.get(user=self.chef)

        self.workshop = Workshop.objects.create(
            chef=chef,
            title="Test Workshop",
            description="This is a test workshop.",
            date=date.today(),
            time=time(14, 30),
            capacity=10,
            price=100.00,
        )

        self.client.force_login(self.customer)

    def test_view_renders_correct_workshop_for_customer(self):
        url = reverse("cust-workshop-detail", kwargs={"id": self.workshop.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["workshop"].id, self.workshop.id)
        self.assertEqual(response.context["workshop"].title, "Test Workshop")
        self.assertContains(response, "Test Workshop")
        self.assertContains(response, "This is a test workshop.")


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
