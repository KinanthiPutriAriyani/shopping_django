# Generated by Django 4.2.16 on 2024-09-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_category_alter_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
    ]
