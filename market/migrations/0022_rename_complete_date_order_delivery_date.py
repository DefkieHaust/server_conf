# Generated by Django 4.2 on 2023-04-08 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0021_alter_order_delivered_alter_order_payment_received"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="complete_date",
            new_name="delivery_date",
        ),
    ]