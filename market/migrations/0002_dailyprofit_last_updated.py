# Generated by Django 4.2 on 2023-04-20 19:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dailyprofit",
            name="last_updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
