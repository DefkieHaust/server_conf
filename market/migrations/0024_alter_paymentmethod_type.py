# Generated by Django 4.2 on 2023-04-09 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0023_paymentmethod_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentmethod",
            name="type",
            field=models.CharField(
                choices=[("crypto", "crypto"), ("bank", "bank"), ("cash", "cash")],
                max_length=20,
            ),
        ),
    ]