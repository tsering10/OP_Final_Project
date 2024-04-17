from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef


class ChefModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user, _ = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="chefjohn",
            email="chefjohn@example.com",
            password="testpass123",
        )
        user.role = User.CHEF
        user.is_active = True
        user.save()

        user_profile, _ = UserProfile.objects.get_or_create(user=user)

        # Create the chef instance
        cls.chef = Chef.objects.create(
            user=user,
            user_profile=user_profile,
            chef_name="Chef John",
            chef_license=SimpleUploadedFile(
                "license.jpg", b"license file content", content_type="image/jpeg"
            ),
            is_approved=True,
        )

    def test_chef_creation(self):
        self.assertTrue(isinstance(self.chef, Chef))
        self.assertEqual(self.chef.chef_name, "Chef John")
