from datetime import date, time

from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.workshop.models import Workshop, WorkshopRegistration


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
        user_profile, _ = UserProfile.objects.get_or_create(user=user)

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
