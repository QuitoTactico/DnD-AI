# Generated by Django 5.0.1 on 2024-03-17 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DnD_AI", "0008_alter_character_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="character",
            name="inventory",
            field=models.TextField(default="{}"),
        ),
        migrations.AddField(
            model_name="monster",
            name="inventory",
            field=models.TextField(default="{'gold': 10}"),
        ),
        migrations.AlterField(
            model_name="monster",
            name="name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
