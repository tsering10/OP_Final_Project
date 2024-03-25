from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from efood_main.apps.accounts.forms import UserForm, UserProfileForm


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


class UserProfileFormTest(TestCase):
    def test_invalid_file_types(self):
        """Test the form with invalid file types
        for profile_picture and cover_photo."""
        invalid_files = {
            "profile_picture": SimpleUploadedFile(
                "invalid_profile.txt",
                b"This is not an image file.",
                content_type="text/plain",
            ),
            "cover_photo": SimpleUploadedFile(
                "invalid_cover.txt",
                b"This is also not an image file.",
                content_type="text/plain",
            ),
        }
        valid_data = {
            "address": "123 Main St",
            "city": "Anytown",
            "country": "USA",
            "state": "State",
            "postal_code": "12345",
        }
        form = UserProfileForm(data=valid_data, files=invalid_files)
        self.assertFalse(form.is_valid())
        self.assertIn("profile_picture", form.errors)
        self.assertIn("cover_photo", form.errors)
        self.assertEqual(
            form.errors["profile_picture"],
            ["invalid_profile.txt is not a valid image format"],
        )

    def test_form_field_existence(self):
        """Test that all expected fields
        are present and of the correct type."""
        form = UserProfileForm()
        expected_fields = {
            "profile_picture": "FileField",
            "cover_photo": "FileField",
            "address": "CharField",
            "city": "CharField",
            "country": "CharField",
            "state": "CharField",
            "postal_code": "CharField",
        }
        for field_name, field_type in expected_fields.items():
            self.assertIn(field_name, form.fields)
            self.assertEqual(type(form.fields[field_name]).__name__, field_type)

    def test_valid_data(self):
        """Test the form with valid data, including file uploads."""
        valid_data = {
            "address": "123 Main St",
            "city": "Anytown",
            "country": "USA",
            "state": "State",
            "postal_code": "12345",
        }
        valid_files = {
            "profile_picture": SimpleUploadedFile(
                "profile.jpg", b"file_content", content_type="image/jpeg"
            ),
            "cover_photo": SimpleUploadedFile(
                "cover.jpg", b"file_content", content_type="image/jpeg"
            ),
        }
        form = UserProfileForm(data=valid_data, files=valid_files)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """Test the form with invalid data to trigger validation errors."""
        invalid_data = {
            "address": "",
            "city": "",
        }
        form = UserProfileForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("profile_picture", form.errors)
        self.assertIn("cover_photo", form.errors)

    def test_form_saves_correctly(self):
        """Test that the form saves correctly when given valid data."""
        valid_data = {
            "address": "123 Main St",
            "city": "Anytown",
            "country": "USA",
            "state": "State",
            "postal_code": "12345",
        }
        valid_files = {
            "profile_picture": SimpleUploadedFile(
                "profile.jpg", b"file_content", content_type="image/jpeg"
            ),
            "cover_photo": SimpleUploadedFile(
                "cover.jpg", b"file_content", content_type="image/jpeg"
            ),
        }
        form = UserProfileForm(data=valid_data, files=valid_files)
        if form.is_valid():
            user_profile = form.save()
            self.assertIsNotNone(user_profile.id)  # Check the object was saved
        else:
            self.fail("Form should be valid and save the instance")
