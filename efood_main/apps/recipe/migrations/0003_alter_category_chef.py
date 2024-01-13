# Generated by Django 4.2.6 on 2024-01-05 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chef", "0002_alter_chef_user"),
        ("recipe", "0002_alter_category_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="chef",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories",
                to="chef.chef",
            ),
        ),
    ]