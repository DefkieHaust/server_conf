# Generated by Django 4.2 on 2023-04-07 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("market", "0012_orderitem_remove_cart_user_delete_completeorder_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
