# Generated by Django 5.0.2 on 2024-04-21 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DnD_AI', '0020_history_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='image',
        ),
    ]