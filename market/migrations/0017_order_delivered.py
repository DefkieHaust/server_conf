# Generated by Django 4.2 on 2023-04-08 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0016_order_payment_received"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivered",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
