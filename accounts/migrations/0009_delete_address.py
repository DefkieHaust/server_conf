# Generated by Django 4.2 on 2023-04-21 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0003_alter_order_address"),
        ("accounts", "0008_user_local"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Address",
        ),
    ]
