# Generated by Django 4.0.1 on 2022-04-11 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0036_migrate_responsibilities_to_app'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Responsibility',
        ),
    ]
