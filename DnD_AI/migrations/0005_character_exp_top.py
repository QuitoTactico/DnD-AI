# Generated by Django 5.0.1 on 2024-03-07 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DnD_AI', '0004_weapon_range_level_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='exp_top',
            field=models.IntegerField(default=30),
        ),
    ]