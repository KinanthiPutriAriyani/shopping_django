# Generated by Django 4.2.16 on 2024-09-25 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_alter_product_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("username", models.CharField(max_length=50, unique=True)),
                ("password", models.CharField(max_length=6)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("date_of_birth", models.DateField()),
                ("gender", models.CharField(max_length=10)),
                ("address", models.TextField()),
                ("city", models.CharField(max_length=50)),
                ("contact_no", models.CharField(max_length=15)),
                ("paypal_id", models.CharField(max_length=100)),
            ],
        ),
    ]
