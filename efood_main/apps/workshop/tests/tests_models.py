from datetime import date, time

from django.test import TestCase

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.workshop.models import Workshop, WorkshopRegistration


class BaseTest(TestCase):
    def setUp(self):
        # Create two users: a regular user and a chef
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.chef_user, _ = User.objects.get_or_create(
            first_name="Chef",
            last_name="Test",
            username="cheftest",
            email="cheftest@example.com",
            password="testpass",
        )
        # Create UserProfile instances for each user
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.chef_user_profile, _ = UserProfile.objects.get_or_create(
            user=self.chef_user
        )
        # Create a Chef instance linked to the chef_user
        self.chef = Chef.objects.create(
            user=self.chef_user,
            user_profile=self.chef_user_profile,
            chef_name="TestChef",
        )

        # Create a workshop hosted by the chef
        self.workshop = Workshop.objects.create(
            chef=self.chef,
            title="Cooking Basics",
            description="Learn the basics of cooking.",
            date=date.today(),
            time=time(10, 0),
            capacity=20,
            price=50.00,
        )


class WorkshopModelTest(BaseTest):
    def test_workshop_creation(self):
        workshop = Workshop.objects.get(title="Cooking Basics")
        self.assertTrue(isinstance(workshop, Workshop))
        self.assertEqual(workshop.__str__(), "Cooking Basics")


class WorkshopRegistrationModelTest(BaseTest):
    def setUp(self):
        super().setUp()  # Call the base class to set up the initial objects
        # Register the user to the workshop
        WorkshopRegistration.objects.create(customer=self.user, workshop=self.workshop)

    def test_workshop_registration(self):
        registration = WorkshopRegistration.objects.get(customer__username="testuser")
        self.assertTrue(isinstance(registration, WorkshopRegistration))
        self.assertEqual(registration.workshop.title, "Cooking Basics")
        self.assertEqual(registration.workshop.capacity, 20)
        self.assertFalse(registration.is_canceled)
