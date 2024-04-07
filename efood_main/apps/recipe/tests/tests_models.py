from datetime import timedelta

from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.models import Category, RecipeItem


class BaseTest(TestCase):
    def setUp(self):
        # Create a user
        self.user, _ = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="testuser",
            email="user@example.com",
            password="testpass123",
        )
        # Create a user profile
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)
        # Create a chef
        self.chef = Chef.objects.create(
            user=self.user, user_profile=self.user_profile, chef_name="Chef Test"
        )

    def create_category(self, chef, category_name, slug):
        return Category.objects.create(
            chef=chef, category_name=category_name, slug=slug
        )

    def create_recipe_item(
        self, chef, category, title, slug, ingredients, instructions, prep_time
    ):
        return RecipeItem.objects.create(
            chef=chef,
            category=category,
            recipe_title=title,
            slug=slug,
            recipe_ingredients=ingredients,
            recipe_instructions=instructions,
            preparation_time=prep_time,
        )


class CategoryModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category = self.create_category(self.chef, "Vegan", "vegan")

    def test_category_creation(self):
        category = Category.objects.get(slug="vegan")
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), "Vegan")

    def test_category_name_capitalization(self):
        # Check if the category name has been capitalized correctly
        self.category.category_name = "vegan"  # Simulate lowercase input
        self.category.clean()  # Call the clean method to capitalize
        self.assertEqual(
            self.category.category_name,
            "Vegan",
            "The category_name should have been capitalized",
        )


class RecipeItemModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        category = self.create_category(self.chef, "Vegetarian", "vegetarian")
        self.recipe_item = self.create_recipe_item(
            chef=self.chef,
            category=category,
            title="Quinoa Salad",
            slug="quinoa-salad",
            ingredients="Quinoa, Tomatoes, Cucumber, Olive oil, Lemon",
            instructions="Mix ingredients in a bowl. Serve chilled.",
            prep_time=timedelta(minutes=30),
        )

    def test_recipe_item_creation(self):
        self.assertTrue(isinstance(self.recipe_item, RecipeItem))
        self.assertEqual(self.recipe_item.__str__(), "Quinoa Salad")
        self.assertEqual(
            self.recipe_item.formatted_preparation_time, "00 hr:30 min:00 sec"
        )
