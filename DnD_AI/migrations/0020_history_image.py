# Generated by Django 5.0.2 on 2024-04-21 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DnD_AI", "0019_tile_campaign"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="image",
            field=models.CharField(default="illustrations/test.png/", max_length=50),
        ),
    ]
