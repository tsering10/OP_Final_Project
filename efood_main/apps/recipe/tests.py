from datetime import timedelta

from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.models import RecipeItem

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
        # user = User.objects.create_user("chefuser", "chef@example.com", "testpass")
        # user_profile = UserProfile.objects.create(user=user)
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
            recipe_ingredients="Quinoa, Tomatoes, Cucumber, Olive oil, Lemon juice",
            recipe_instructions="Mix all ingredients in a bowl. Serve chilled.",
            preparation_time=timedelta(minutes=30),
        )

    def test_recipe_item_creation(self):
        recipe_item = RecipeItem.objects.get(slug="quinoa-salad")
        self.assertTrue(isinstance(recipe_item, RecipeItem))
        self.assertEqual(recipe_item.__str__(), "Quinoa Salad")
        self.assertEqual(recipe_item.formatted_preparation_time, "00 hr:30 min:00 sec")
