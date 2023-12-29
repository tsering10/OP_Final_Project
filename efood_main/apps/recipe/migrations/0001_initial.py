# Generated by Django 4.2.6 on 2023-12-28 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("chef", "0002_alter_chef_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=50)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "chef",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chef.chef"
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="RecipeItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recipe_title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("recipe_ingredients", models.TextField()),
                ("recipe_instructions", models.TextField()),
                ("preparation_time", models.DurationField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="recipe_images/"
                    ),
                ),
                ("external_link", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipeitems",
                        to="recipe.category",
                    ),
                ),
                (
                    "chef",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chef.chef"
                    ),
                ),
            ],
        ),
    ]
