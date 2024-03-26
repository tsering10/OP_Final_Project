from datetime import date, time, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.models import Category, RecipeItem
from efood_main.apps.workshop.forms import WorkshopItemForm

from .models import Workshop, WorkshopRegistration


class WorkshopItemFormTest(TestCase):
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


class WorkshopModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        # Create a UserProfile for the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Create a Chef instance, ensuring to link both User and UserProfile
        Chef.objects.create(user=user, user_profile=user_profile, chef_name="TestChef")

        chef = Chef.objects.get(user=user)

        Workshop.objects.create(
            chef=chef,
            title="Test Workshop",
            description="This is a test workshop.",
            date=date.today(),
            time=time(14, 30),
            capacity=10,
            price=100.00,
        )

    def test_workshop_creation(self):
        workshop = Workshop.objects.get(title="Test Workshop")
        self.assertTrue(isinstance(workshop, Workshop))
        self.assertEqual(workshop.__str__(), "Test Workshop")


class WorkshopRegistrationModelTest(TestCase):
    def setUp(self):
        # Create user, chef, workshop, and register user to the workshop
        user, _ = User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="password",
        )
        chef_user, _ = User.objects.get_or_create(
            first_name="Chef",
            last_name="Test",
            username="cheftest",
            email="cheftest@example.com",
            password="testpass",
        )
        chef_user_profile, _ = UserProfile.objects.get_or_create(user=chef_user)
        Chef.objects.create(
            user=chef_user, user_profile=chef_user_profile, chef_name="Test Chef"
        )

        chef = Chef.objects.get(user=chef_user)
        workshop = Workshop.objects.create(
            chef=chef,
            title="Cooking Basics",
            description="Learn the basics of cooking.",
            date=date.today(),
            time=time(10, 0),
            capacity=20,
            price=50.00,
        )
        WorkshopRegistration.objects.create(customer=user, workshop=workshop)

    def test_workshop_registration(self):
        registration = WorkshopRegistration.objects.get(customer__username="johndoe")
        self.assertTrue(isinstance(registration, WorkshopRegistration))
        self.assertEqual(registration.workshop.title, "Cooking Basics")
        self.assertEqual(registration.workshop.capacity, 20)
        self.assertFalse(registration.is_canceled)
