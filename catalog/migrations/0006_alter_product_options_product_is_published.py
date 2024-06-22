# Generated by Django 4.2.2 on 2024-06-20 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_product_maker"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "permissions": [
                    ("can_edit_category", "Can edit category"),
                    ("can_edit_description", "Can edit description"),
                    ("can_off_published", "Can off published"),
                ],
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="опубликовано"),
        ),
    ]