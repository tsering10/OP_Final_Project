from django.test import Client, TestCase
from django.urls import reverse


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
