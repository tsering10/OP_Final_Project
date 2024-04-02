from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from efood_main.apps.accounts.models import User


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

    def test_login_post_invalid_credentials(self):
        url = reverse("login")
        data = {
            "email": "user@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ActivateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            first_name="john",
            last_name="doe",
            email="testuser@example.com",
            password="test1234",
            is_active=False,
            role=1,
        )

    def test_activate_success(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("activate", args=[uid, token])
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertRedirects(response, reverse("login"))
