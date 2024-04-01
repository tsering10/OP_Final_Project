from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile

from .models import Chef


class ChefModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a custom user for the chef
        user, created = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="chefjohn",
            email="chefjohn@example.com",
            password="testpass123",
        )
        user.role = User.CHEF
        user.is_active = True
        user.save()

        # Create a user profile associated with the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Create the chef instance
        cls.chef = Chef.objects.create(
            user=user,
            user_profile=user_profile,
            chef_name="Chef John",
            chef_license=SimpleUploadedFile(
                "license.jpg", b"license file content", content_type="image/jpeg"
            ),
            is_approved=True,
            # Fill in other required fields as needed
        )

    def test_chef_creation(self):
        # Validate the Chef instance.
        self.assertTrue(isinstance(self.chef, Chef))
        self.assertEqual(self.chef.chef_name, "Chef John")
