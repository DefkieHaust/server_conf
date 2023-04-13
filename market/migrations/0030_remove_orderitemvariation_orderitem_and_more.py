# Generated by Django 4.2 on 2023-04-13 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0029_remove_cartitem_amount_remove_orderitem_amount_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitemvariation",
            name="orderitem",
        ),
        migrations.RemoveField(
            model_name="orderitemvariation",
            name="variation",
        ),
        migrations.AddField(
            model_name="cartitem",
            name="amount",
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="orderitem",
            name="amount",
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="market.variation"
            ),
        ),
        migrations.DeleteModel(
            name="CartItemVariation",
        ),
        migrations.DeleteModel(
            name="OrderItemVariation",
        ),
    ]
