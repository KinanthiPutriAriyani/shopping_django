# Generated by Django 4.2.16 on 2024-09-25 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart", name="username", field=models.CharField(max_length=255),
        ),
    ]
