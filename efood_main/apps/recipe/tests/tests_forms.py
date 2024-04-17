from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.forms import CategoryForm, RecipeItemForm
from efood_main.apps.recipe.models import Category


class CategoryFormTest(TestCase):
    def test_category_form_valid(self):
        form_data = {"category_name": "Desserts", "description": "Sweets"}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        form_data = {}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())


class RecipeItemFormTest(TestCase):
    def setUp(self):
        user, _ = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="chefjohn",
            email="chefjohn@example.com",
            password="testpass123",
        )
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        self.chef = Chef.objects.create(
            user=user, user_profile=user_profile, chef_name="Chef John"
        )

        self.category = Category.objects.create(
            category_name="Main Course", description="Main dishes", chef=self.chef
        )
        self.image_file = {
            "image": SimpleUploadedFile(
                "image.jpg", b"file_content", content_type="image/jpeg"
            ),
        }

    def test_recipe_item_form_valid(self):
        form_data = {
            "category": self.category.id,
            "recipe_title": "Spaghetti Carbonara",
            "recipe_ingredients": "Pasta, Eggs, Parmesan, Bacon",
            "recipe_instructions": "Cook pasta, mix with other ingredients",
            "preparation_time": "00:30:00",
            "external_link": "http://example.com",
            "image": self.image_file,
        }
        form = RecipeItemForm(data=form_data, files=self.image_file)
        self.assertTrue(form.is_valid())

    def test_preparation_time_invalid_format(self):
        form_data = {
            "category": self.category.id,
            "recipe_title": "Lasagna",
            "recipe_ingredients": "Ingredients here",
            "recipe_instructions": "Instructions here",
            "preparation_time": "2 hours",
            "external_link": "http://example.com",
            "image": self.image_file,
        }
        form = RecipeItemForm(data=form_data, files=self.image_file)
        self.assertFalse(form.is_valid())
        self.assertIn("preparation_time", form.errors)
