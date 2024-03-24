from django.test import TestCase

from efood_main.apps.accounts.forms import UserForm


class UserFormTestCase(TestCase):
    def test_password_confirmation_failure(self):
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password1",
            "confirm_password": "password2",
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Password does not match!", form.errors["__all__"])

    def test_valid_data(self):
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "confirm_password": "password",
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_role_assignment_on_save(self):
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "confirm_password": "password",
        }
        form = UserForm(data=form_data)
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.role, user.CUSTOMER)
