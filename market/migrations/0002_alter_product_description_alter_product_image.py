# Generated by Django 4.2 on 2023-04-05 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]
