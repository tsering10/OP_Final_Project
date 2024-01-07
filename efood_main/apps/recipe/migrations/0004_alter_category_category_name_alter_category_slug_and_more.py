# Generated by Django 4.2.6 on 2024-01-07 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chef", "0002_alter_chef_user"),
        ("recipe", "0003_alter_category_chef"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name="category",
            unique_together={("chef", "category_name")},
        ),
    ]
