from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from efood_main.apps.accounts.models import User, UserProfile


class TestRegisterUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("registerUser"))

    def test_display_register_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/registerUser.html")
        self.assertContains(self.response, "first_name")
        self.assertContains(self.response, "last_name")
        self.assertContains(self.response, "email")
        self.assertContains(self.response, "password")


class TestRegisterChefView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("registerChef"))

    def test_display_register_chef_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/registerChef.html")
        self.assertContains(self.response, "first_name")
        self.assertContains(self.response, "last_name")
        self.assertContains(self.response, "chef_name")
        self.assertContains(self.response, "chef_license")
        self.assertContains(self.response, "email")
        self.assertContains(self.response, "password")


class LoginViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            first_name="jojo",
            last_name="wowo",
            username="TestJo",
        )

    def test_login_page(self):
        """
        Test login page loads correctly.
        """
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_successful_login(self):
        """
        Test logging in with correct credentials.
        """
        url = reverse("login")
        data = {
            "email": "test@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(url, data)
        self.assertRedirects(
            response,
            expected_url=reverse("login"),
            status_code=302,
            target_status_code=200,
        )
