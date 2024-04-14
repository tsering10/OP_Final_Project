from datetime import timedelta

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from efood_main.apps.accounts.models import User, UserProfile
from efood_main.apps.chef.models import Chef
from efood_main.apps.recipe.models import Category, RecipeItem


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="chefuser",
            email="chef@example.com",
            password="chefpassword",
            first_name="Test",
            last_name="Chef",
            role=1,
            is_active=True,
        )
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.chef = Chef.objects.create(
            user=self.user,
            user_profile=self.user_profile,
            chef_name="Test Chef",
            chef_license=SimpleUploadedFile(
                name="test_license.jpg", content=b"", content_type="image/jpeg"
            ),
            is_approved=True,
        )
        self.mock_image_file = SimpleUploadedFile(
            name="test_image.jpg", content=b"test image data", content_type="image/jpeg"
        )
        self.client.force_login(self.user)


class ChefProfileViewTest(BaseTest):

    def test_chef_profile_view_get(self):
        response = self.client.get(reverse("chef_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["combined_form"]["profile_form"].instance)
        self.assertIsNotNone(response.context["combined_form"]["chef_form"].instance)
        self.assertEqual(response.context["profile"], self.user_profile)
        self.assertEqual(response.context["chef"], self.chef)

    def test_chef_profile_view_post(self):
        # Prepare valid data for your UserProfileForm and UserInfoForm
        profile_picture = SimpleUploadedFile(
            "profile_pic.jpg", b"file_content", content_type="image/jpeg"
        )
        cover_photo = SimpleUploadedFile(
            "cover_photo.jpg", b"file_content", content_type="image/jpeg"
        )
        chef_license = SimpleUploadedFile(
            name="new_chef_license.jpg",
            content=b"test content",
            content_type="image/jpeg",
        )

        valid_data = {
            "chef_name": "TestChef",
            "chef_license": chef_license,
            "profile_picture": profile_picture,
            "cover_photo": cover_photo,
            "address": "123 Main St",
            "city": "Anytown",
            "country": "USA",
            "state": "Texas",
            "postal_code": "12345",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
        }
        response = self.client.post(reverse("chef_profile"), data=valid_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Profile updated.", [message.message for message in messages])


class RecipeItemsByCategoryViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(
            chef=self.chef, category_name="Category 1", slug="category-1"
        )

        self.category2 = Category.objects.create(
            chef=self.chef, category_name="Category 2", slug="category-2"
        )

        self.recipe_item1 = RecipeItem.objects.create(
            chef=self.chef,
            category=self.category1,
            recipe_title="Item 1",
            slug="item-1",
            recipe_ingredients="Ingredients 1",
            recipe_instructions="Instructions 1",
            preparation_time=timedelta(minutes=10),
            image=self.mock_image_file,
        )
        self.recipe_item2 = RecipeItem.objects.create(
            chef=self.chef,
            category=self.category1,
            recipe_title="Item 2",
            slug="item-2",
            recipe_ingredients="Ingredients 2",
            recipe_instructions="Instructions 2",
            preparation_time=timedelta(minutes=20),
            image=self.mock_image_file,
        )

    def test_recipe_items_by_category_view(self):
        response = self.client.get(
            reverse("recipeitems_by_category", kwargs={"pk": self.category1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.recipe_item1, response.context["recipeitems"])
        self.assertIn(self.recipe_item2, response.context["recipeitems"])
        self.assertEqual(response.context["category"], self.category1)


class ChefRecipeBuilderTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(
            chef=self.chef, category_name="Category 1", slug="category-1"
        )

        self.category2 = Category.objects.create(
            chef=self.chef, category_name="Category 2", slug="category-2"
        )

    def test_chef_recipe_builder_view(self):
        response = self.client.get(reverse("recipe_builder"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category1, response.context["categories"])
        self.assertIn(self.category2, response.context["categories"])


class AddCategoryViewTest(BaseTest):
    def setUp(self):
        super().setUp()

    def test_add_category(self):
        url = reverse("add_category")
        category_name = "New Category"
        data = {
            "category_name": category_name,
            "description": "A new category description.",
        }

        response = self.client.post(url, data)
        self.assertRedirects(
            response, reverse("recipe_builder"), status_code=302, target_status_code=200
        )
        category = Category.objects.first()
        self.assertIsNotNone(category)
        self.assertEqual(category.slug, slugify(category_name))


class EditCategoryViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(
            chef=self.chef, category_name="Original Category", slug="original-category"
        )

    def test_edit_category(self):
        url = reverse("edit_category", kwargs={"pk": self.category.pk})
        updated_name = "Updated Category"
        data = {
            "category_name": updated_name,
            "description": "Updated category description.",
        }

        response = self.client.post(url, data)

        self.assertRedirects(
            response, reverse("recipe_builder"), status_code=302, target_status_code=200
        )

        self.category.refresh_from_db()
        self.assertEqual(self.category.category_name, updated_name.capitalize())
        self.assertEqual(self.category.slug, slugify(updated_name))
        messages = [msg for msg in response.wsgi_request._messages]

        self.assertTrue(
            any(msg.message == "Category updated successfully!" for msg in messages)
        )


class AddRecipeViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(
            chef=self.chef, category_name="Test Category", slug="test-category"
        )

    def test_add_recipe(self):
        # Prepare data for a new recipe item
        recipe_title = "Delicious Test Recipe"
        mock_image_file = SimpleUploadedFile(
            name="test_image.jpg", content=b"test image data", content_type="image/jpeg"
        )
        data = {
            "recipe_title": recipe_title,
            "category": self.category.id,
            "recipe_ingredients": "Ingredient 1, Ingredient 2",
            "recipe_instructions": "Step 1, Step 2",
            "preparation_time": timedelta(minutes=30),
            "image": mock_image_file,
        }

        url = reverse("add_recipe")

        response = self.client.post(url, data)
        self.assertRedirects(
            response,
            reverse("recipeitems_by_category", args=(self.category.id,)),
            status_code=302,
        )
        # Fetch the added recipe item
        recipe_item = RecipeItem.objects.first()
        self.assertIsNotNone(recipe_item)
        self.assertEqual(recipe_item.slug, slugify(recipe_title))
        self.assertEqual(
            response.status_code,
            302,
            "The form submission did not redirect as expected.",
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                message.message == "Recipe Item added successfully!"
                for message in messages
            ),
            "Success message was not found in messages.",
        )


class EditRecipeViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(
            chef=self.chef, category_name="Test Category", slug="test-category"
        )

        self.recipe_item = RecipeItem.objects.create(
            chef=self.chef,
            category=self.category,
            recipe_title="Item 2",
            slug="item-2",
            recipe_ingredients="Ingredients 2",
            recipe_instructions="Instructions 2",
            preparation_time=timedelta(minutes=20),
            image=self.mock_image_file,
        )

    def test_edit_recipe(self):
        url = reverse("edit_recipe", kwargs={"pk": self.recipe_item.pk})
        updated_data = {
            "recipe_title": "Updated Recipe Title",
            "recipe_ingredients": "Updated Ingredients",
            "recipe_instructions": "Updated Instructions",
            "preparation_time": "00:45:00",
            "category": self.category.id,
        }
        # Perform the POST request to update the recipe
        response = self.client.post(url, updated_data)
        self.assertRedirects(
            response,
            reverse("recipeitems_by_category", args=[self.category.id]),
            status_code=302,
        )
        # Fetch the updated recipe item
        self.recipe_item.refresh_from_db()
        self.assertEqual(self.recipe_item.recipe_title, updated_data["recipe_title"])
        self.assertEqual(self.recipe_item.slug, slugify(updated_data["recipe_title"]))


class RecipeDetailViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(
            chef=self.chef, category_name="Test Category", slug="test-category"
        )
        self.recipe = RecipeItem.objects.create(
            chef=self.chef,
            category=self.category,
            recipe_title="Item 2",
            slug="item-2",
            recipe_ingredients="Ingredients 2",
            recipe_instructions="Instructions 2",
            preparation_time=timedelta(minutes=20),
            image=self.mock_image_file,
        )

    def test_recipe_detail_view_with_valid_recipe(self):
        response = self.client.get(
            reverse(
                "recipe_detail", kwargs={"slug": self.recipe.slug, "id": self.recipe.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chef/recipe_detail.html")
        self.assertEqual(response.context["recipe"], self.recipe)
