# Generated by Django 4.2 on 2023-04-11 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0028_alter_order_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="amount",
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="market.product"
            ),
        ),
        migrations.CreateModel(
            name="OrderItemVariation",
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
                ("amount", models.IntegerField()),
                (
                    "orderitem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variations",
                        to="market.orderitem",
                    ),
                ),
                (
                    "variation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="market.variation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CartItemVariation",
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
                ("amount", models.IntegerField()),
                (
                    "cartitem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variations",
                        to="market.cartitem",
                    ),
                ),
                (
                    "variation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="market.variation",
                    ),
                ),
            ],
        ),
    ]
