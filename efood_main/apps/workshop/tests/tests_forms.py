from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.models import Category, RecipeItem
from efood_main.apps.workshop.forms import WorkshopItemForm


class WorkshopItemFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a custom user for the chef
        user, _ = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="chefjohn",
            email="chefjohn@example.com",
            password="testpass123",
            is_active=True,
            role=1,
        )

        # Create a user profile associated with the user
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
            # Fill in other required fields as needed
        )

        # Create a category for the recipes
        category = Category.objects.create(
            chef=cls.chef,
            category_name="Desserts",
            slug="desserts",
            description="Sweet treats",
        )

        # Add recipe items to the chef within the created category
        RecipeItem.objects.create(
            chef=cls.chef,
            category=category,
            recipe_title="Chocolate Cake",
            slug="chocolate-cake",
            recipe_ingredients="Chocolate, Flour, Sugar, Eggs",
            recipe_instructions="Mix ingredients and bake.",
            preparation_time=timedelta(minutes=45),
            # Optionally add image and external link
        )

        RecipeItem.objects.create(
            chef=cls.chef,
            category=category,
            recipe_title="Lemon Tart",
            slug="lemon-tart",
            recipe_ingredients="Lemon, Flour, Sugar, Eggs",
            recipe_instructions="Mix ingredients and bake.",
            preparation_time=timedelta(minutes=30),
        )

    def test_form_with_valid_data(self):
        form_data = {
            "title": "Test Workshop",
            "description": "A test workshop",
            "date": "2024-03-25",
            "time": "14:00",
            "capacity": 20,
            "address": "123 Main St",
            "latitude": "40.7128",
            "longitude": "-74.0060",
            "price_0": 10,  # The amount
            "price_1": "EUR",  # The currency code
            "contact_phone": "1234567890",
            "recipe": RecipeItem.objects.first().id,
        }
        form = WorkshopItemForm(data=form_data, chef=self.chef)
        self.assertTrue(form.is_valid())

    def tearDown(self):
        UserProfile.objects.all().delete()  # Or more targeted cleanup
        User.objects.all().delete()
