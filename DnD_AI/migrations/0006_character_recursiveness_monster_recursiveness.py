# Generated by Django 5.0.1 on 2024-03-08 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DnD_AI", "0005_character_exp_top"),
    ]

    operations = [
        migrations.AddField(
            model_name="character",
            name="recursiveness",
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name="monster",
            name="recursiveness",
            field=models.IntegerField(default=10),
        ),
    ]
