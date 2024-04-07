from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from efood_main.apps.accounts.models import User, UserProfile


class TestRegisterUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("registerUser"))

    def test_display_register_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/registerUser.html")
        self.assertContains(self.response, "first_name")
        self.assertContains(self.response, "last_name")
        self.assertContains(self.response, "email")
        self.assertContains(self.response, "password")


class TestRegisterChefView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("registerChef"))

    def test_display_register_chef_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/registerChef.html")
        self.assertContains(self.response, "first_name")
        self.assertContains(self.response, "last_name")
        self.assertContains(self.response, "chef_name")
        self.assertContains(self.response, "chef_license")
        self.assertContains(self.response, "email")
        self.assertContains(self.response, "password")


class LoginViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            first_name="jojo",
            last_name="wowo",
            username="TestJo",
        )

    def test_login_page(self):
        """
        Test login page loads correctly.
        """
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_successful_login(self):
        """
        Test logging in with correct credentials.
        """
        url = reverse("login")
        data = {
            "email": "test@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(url, data)
        self.assertRedirects(
            response,
            expected_url=reverse("login"),
            status_code=302,
            target_status_code=200,
        )

    def test_login_post_invalid_credentials(self):
        url = reverse("login")
        data = {
            "email": "user@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="customeruser",
            email="customer@example.com",
            password="customerpassword",
            first_name="Test",
            last_name="customer",
            role=2,
            is_active=True,
        )
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def test_logout(self):
        # Perform a GET request to the logout view
        response = self.client.get(reverse("logout"))

        # After logout, the user should be an AnonymousUser
        self.assertTrue(
            response.wsgi_request.user.is_anonymous, "User is not logged out."
        )
        self.assertRedirects(response, reverse("home"), status_code=302)
        # Verify the logout message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(message.message == "You are logged out." for message in messages),
            "Logout message was not found.",
        )


class ActivateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            first_name="john",
            last_name="doe",
            email="testuser@example.com",
            password="test1234",
            is_active=False,
            role=1,
        )

    def test_activate_success(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("activate", args=[uid, token])
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertRedirects(response, reverse("login"))

    def test_activate_invalid(self):
        url = reverse("activate", args=["bad-uid", "bad-token"])
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)


class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        self.forgot_password_url = reverse("forgot_password")
        self.login_url = reverse("login")
        self.user = User.objects.create(
            username="customeruser",
            email="customer@example.com",
            password="customerpassword",
            first_name="Test",
            last_name="customer",
            role=2,
            is_active=True,
        )
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_get_forgot_password_page(self):
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/forgot_password.html")


class ResetPasswordValidateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="customeruser",
            email="customer@example.com",
            password="customerpassword",
            first_name="Test",
            last_name="customer",
            role=2,
            is_active=True,
        )
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.uid = urlsafe_base64_encode(force_str(self.user.pk).encode())
        self.token = default_token_generator.make_token(self.user)
        self.valid_url = reverse(
            "reset_password_validate", kwargs={"uidb64": self.uid, "token": self.token}
        )
        self.invalid_url = reverse(
            "reset_password_validate", kwargs={"uidb64": "MjM", "token": "abcd-efgh"}
        )

    def test_valid_uid_token(self):
        response = self.client.get(self.valid_url)
        self.assertRedirects(response, reverse("reset_password"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(msg.message == "Please reset your password" for msg in messages)
        )
        self.assertEqual(self.client.session["uid"], force_str(self.user.pk))

    def test_invalid_uid_token(self):
        response = self.client.get(self.invalid_url)
        self.assertRedirects(response, reverse("forgot_password"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(msg.message == "This link has been expired!" for msg in messages)
        )


class RegisterUserViewTestCase(TestCase):
    def setUp(self):
        # Setup request data for user registration
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password1",
            "confirm_password": "password2",
        }

    def test_register_user_form_valid(self):
        response = self.client.post(reverse("registerUser"), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_name")
        self.assertTemplateUsed(response, "accounts/registerUser.html")

    def test_register_user_form_invalid(self):
        # Modify one field to make the form invalid
        invalid_data = self.user_data.copy()
        invalid_data["email"] = ""  # Assuming email is required
        response = self.client.post(reverse("registerUser"), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="").exists())


class RegisterChefViewTestCase(TestCase):
    def setUp(self):
        # Setup request data for chef registration
        self.chef_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password1",
            "confirm_password": "password2",
            "chef_name": "Test Chef",
        }

    def test_register_chef_form_valid(self):
        response = self.client.post(reverse("registerChef"), self.chef_data)
        self.assertContains(response, "chef_name")
        self.assertEqual(response.status_code, 200)

    def test_register_chef_form_invalid(self):
        # Modify one field to make the form invalid
        invalid_data = self.chef_data.copy()
        invalid_data["email"] = ""  # Assuming email is required
        response = self.client.post(reverse("registerChef"), invalid_data)
        self.assertEqual(response.status_code, 200)  # Page reloads with form errors
        self.assertFalse(User.objects.filter(email="").exists())


class CustDashboardViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            first_name="john",
            last_name="doe",
            email="testuser@example.com",
            password="test1234",
            is_active=True,
            role=2,
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)

    def test_customer_dashboard_view(self):
        response = self.client.get(reverse("customerDashboard"))
        self.assertTrue("workshops" in response.context)
        self.assertEqual(response.status_code, 200)


# class ChefDashboardViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             username="chefuser",
#             email="chef@example.com",
#             password="chefpassword",
#             first_name="Test",
#             last_name="Chef",
#             role=1,
#             is_active=True,
#         )

#         self.client.force_login(self.user)
#         # Check if a UserProfile already exists for the user
#         try:
#             self.user_profile = self.user.userprofile
#         except UserProfile.DoesNotExist:
#             # Create a mock profile picture for the user
#             file_content = b"mock_profile_picture_content"
#             uploaded_file = SimpleUploadedFile(
#                 "profile_picture.jpg", file_content, content_type="image/jpeg"
#             )
#             self.user_profile = UserProfile.objects.create(
#                 user=self.user, profile_picture=uploaded_file
#             )

#         self.chef = Chef.objects.create(
#             user=self.user,
#             user_profile=self.user_profile,
#             chef_name="Test Chef",
#             chef_license=SimpleUploadedFile(
#                 name="test_license.jpg", content=b"", content_type="image/jpeg"
#             ),
#             is_approved=True,
#         )

#     def test_get_context_data(self):
#         self.mock_image_file = SimpleUploadedFile(
#             name="test_image.jpg", content=b"test image data", content_type="image/jpeg"
#         )

#         self.category1 = Category.objects.create(
#             chef=self.chef, category_name="Category 1", slug="category-1"
#         )

#         self.recipe_item1 = RecipeItem.objects.create(
#             chef=self.chef,
#             category=self.category1,
#             recipe_title="Item 1",
#             slug="item-1",
#             recipe_ingredients="Ingredients 1",
#             recipe_instructions="Instructions 1",
#             preparation_time=timedelta(minutes=10),
#             image=self.mock_image_file,
#         )

#         url = reverse("chefDashboard")
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)
