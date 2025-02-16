# Generated by Django 5.0.1 on 2024-03-29 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DnD_AI", "0016_tile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="character",
            name="physical_description",
            field=models.CharField(
                default="Masculine, tall, black clothes", max_length=200
            ),
        ),
        migrations.AlterField(
            model_name="monster",
            name="inventory",
            field=models.TextField(default="{'gold': 10, 'health potion': 2}"),
        ),
        migrations.AlterField(
            model_name="monster",
            name="physical_description",
            field=models.CharField(
                default="Masculine, tall, black clothes", max_length=200
            ),
        ),
        migrations.AlterField(
            model_name="monster",
            name="x",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="monster",
            name="y",
            field=models.IntegerField(default=0),
        ),
    ]
