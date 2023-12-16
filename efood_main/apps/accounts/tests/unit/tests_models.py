from django.test import TestCase
from accounts.models import User
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):
    def test_create_user(self): 
        User = get_user_model()
        user = User.objects.create_user(
            username="will", email="will@email.com", password="testpass123",
            first_name="Willy", last_name="Snow"
        )
        self.assertEqual(user.username, "will")
        self.assertEqual(user.email, "will@email.com")


    def test_create_superuser(self):
        User = get_user_model()   
        admin_user = User.objects.create_superuser(
            username="superadmin", email="superadmin@email.com", password="testpass123",
            first_name="john", last_name="thomas"
        ) 
        self.assertEqual(admin_user.username, "superadmin")
        self.assertEqual(admin_user.email, "superadmin@email.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superadmin)
        self.assertIs(admin_user.has_perm("fake permission"), True)     


    def test_customer_chef_role(self):
        self.customer_user = User.objects.create(
            email='customer@example.com',
            username='customer_user',
            first_name='Alice',
            last_name='Johnson',
            role=User.CUSTOMER
        )       

        customer_role = self.customer_user.get_role()
        self.assertEqual(customer_role, 'Customer')

        self.chef = User.objects.create(
            email='chef@example.com',
            username='chef_user',
            first_name='John',
            last_name='Doe',
            role=User.CHEF
        )

        chef_role = self.chef.get_role()
        self.assertEqual(chef_role,'Chef')
