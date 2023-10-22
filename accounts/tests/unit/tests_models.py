from django.test import TestCase, Client
from accounts.models import User
from django.test import RequestFactory


class TestModels(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="inconnu",
            email="inconnu@email.com",
            password="1234AZERTY",
            first_name="john",
            last_name="snow",

        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "inconnu@email.com")
