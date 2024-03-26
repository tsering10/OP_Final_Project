from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.models import RecipeItem

from .forms import CategoryForm, RecipeItemForm
from .models import Category


# Create your tests here.
class CategoryModelTest(TestCase):
    def setUp(self):
        # Create a user and a chef as prerequisites for a category
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

        # Create a category
        Category.objects.create(chef=self.chef, category_name="Vegan", slug="vegan")

    def test_category_creation(self):
        category = Category.objects.get(slug="vegan")
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), "Vegan")

    def test_category_name_capitalization(self):
        # Create a category with a lowercase name
        category = Category.objects.create(
            chef=self.chef, category_name="vegan", slug="vegan"
        )
        # Call the clean method to capitalize the category name
        category.clean()
        # Check if the category name has been capitalized correctly
        self.assertEqual(
            category.category_name,
            "Vegan",
            "The category_name should have been capitalized",
        )


class RecipeItemModelTest(TestCase):
    def setUp(self):
        # Create necessary objects: User, Chef, Category
        user, _ = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="chefuser",
            email="chef@example.com",
            password="testpass",
        )
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        chef = Chef.objects.create(
            user=user, user_profile=user_profile, chef_name="Chef Test"
        )
        category = Category.objects.create(
            chef=chef, category_name="Vegetarian", slug="vegetarian"
        )
        # Create a RecipeItem
        RecipeItem.objects.create(
            chef=chef,
            category=category,
            recipe_title="Quinoa Salad",
            slug="quinoa-salad",
            recipe_ingredients="Quinoa, Tomatoes, Cucumber, Olive oil, Lemon",
            recipe_instructions="Mix ingredients in a bowl. Serve chilled.",
            preparation_time=timedelta(minutes=30),
        )

    def test_recipe_item_creation(self):
        recipe_item = RecipeItem.objects.get(slug="quinoa-salad")
        self.assertTrue(isinstance(recipe_item, RecipeItem))
        self.assertEqual(recipe_item.__str__(), "Quinoa Salad")
        self.assertEqual(recipe_item.formatted_preparation_time, "00 hr:30 min:00 sec")


class CategoryFormTest(TestCase):
    def test_category_form_valid(self):
        form_data = {"category_name": "Desserts", "description": "Sweets"}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        form_data = {}  # Submitting empty data
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())  # Expecting form to be invalid


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
            "preparation_time": "2 hours",  # Intentionally incorrect format
            "external_link": "http://example.com",
            "image": self.image_file,
        }
        form = RecipeItemForm(data=form_data, files=self.image_file)
        self.assertFalse(form.is_valid())
        self.assertIn("preparation_time", form.errors)
