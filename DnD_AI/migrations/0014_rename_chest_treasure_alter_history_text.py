# Generated by Django 5.0.1 on 2024-03-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DnD_AI", "0013_alter_character_icon"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Chest",
            new_name="Treasure",
        ),
        migrations.AlterField(
            model_name="history",
            name="text",
            field=models.CharField(default="Hi (Default message)", max_length=3000),
        ),
    ]
