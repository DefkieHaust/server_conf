# Generated by Django 4.2 on 2023-04-08 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0018_remove_order_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentmethod",
            name="pay_amount",
            field=models.FloatField(blank=True, default=1.0),
        ),
    ]